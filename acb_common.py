#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import numpy as np
from sortedcontainers import SortedList

def dist_tsplib(p1, p2):
    return int(np.sqrt(np.sum((p1 - p2)**2)) + 0.5)

def calcular_angulo_vec(v1, pt, v2):
    a = v1 - pt
    b = v2 - pt
    dot = np.einsum('ij,ij->i', a, b)
    na = np.linalg.norm(a, axis=1)
    nb = np.linalg.norm(b, axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        cos_theta = dot / (na * nb)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        angles = np.degrees(np.arccos(cos_theta))
        angles[np.isnan(angles)] = 180.0
    return angles

def normalize(x):
    x = np.asarray(x, dtype=float)
    denom = np.max(x) - np.min(x)
    if denom == 0:
        return np.zeros_like(x)
    return (x - np.min(x)) / (denom + 1e-9)

def closeness(x, target):
    x = np.asarray(x, dtype=float)
    denom = max(target, 1.0 - target)
    return np.clip(1.0 - np.abs(x - target) / (denom + 1e-9), 0.0, 1.0)

def calcular_candidato_adn(dist_centro, angulos_locales, proximidad_relativa, var_ang_cands):
    dist_n = normalize(dist_centro)
    ang_n = normalize(angulos_locales)
    prox_n = normalize(proximidad_relativa)
    if var_ang_cands < 10000:
        cand_dist = closeness(dist_n, 0.55)
        cand_ang = closeness(ang_n, 0.45)
        cand_prox = closeness(prox_n, 0.60)
        return {
            idx: 0.40 * cand_dist[idx] + 0.30 * cand_ang[idx] + 0.30 * cand_prox[idx]
            for idx in range(len(dist_n))
        }
    return {
        idx: 0.30 * dist_n[idx] + 0.25 * ang_n[idx] + 0.45 * (1.0 - prox_n[idx])
        for idx in range(len(dist_n))
    }

def reordenar_por_adn_geometrico(ciudades_canonicas, offset, phi_perturb):
    n = len(ciudades_canonicas)
    centro = np.mean(ciudades_canonicas, axis=0)
    vec_centro = ciudades_canonicas - centro
    angulos_base = np.arctan2(vec_centro[:, 1], vec_centro[:, 0])
    indices_angulares = np.argsort(angulos_base)
    disponibles = SortedList(range(n))
    orden_final = []
    phi = (1 + np.sqrt(5)) / 2
    angulo_oro_base = 2 - phi
    angulo_oro = (angulo_oro_base + phi_perturb) % 1.0
    for i in range(n):
        proyeccion_ideal = ((i + offset) * angulo_oro) % 1.0
        idx_sugerido = int(proyeccion_ideal * n)
        pos_in_list = disponibles.bisect_left(idx_sugerido)
        if pos_in_list >= len(disponibles):
            idx_elegido = len(disponibles) - 1
        elif pos_in_list == 0:
            idx_elegido = 0
        else:
            c_der, c_izq = disponibles[pos_in_list], disponibles[pos_in_list - 1]
            idx_elegido = pos_in_list if abs(c_der - idx_sugerido) <= abs(c_izq - idx_sugerido) else pos_in_list - 1
        idx_final_angular = disponibles.pop(idx_elegido)
        orden_final.append(indices_angulares[idx_final_angular])
    ruta_indices = np.array(orden_final)
    return ciudades_canonicas[ruta_indices]

def gio_seleccionar_nodo(ciudades, visitados_mask, d_min, inicio_idx, centro, cands_ratio):
    d_min_temp = d_min.copy()
    d_min_temp[visitados_mask] = -1.0
    max_dist = np.max(d_min_temp)
    cands = np.where(d_min_temp > max_dist * cands_ratio)[0]
    if len(cands) == 0:
        cands = np.where(d_min_temp == max_dist)[0]
    rad_ini = np.radians(inicio_idx % 360)
    vector_dir = np.array([np.cos(rad_ini), np.sin(rad_ini)])
    candidatos_relativos = ciudades[cands] - centro
    dir_scores = np.dot(candidatos_relativos, vector_dir)
    idx = int(cands[np.argmax(dir_scores)]) if len(cands) > 1 else int(cands[0])
    return idx

def gio_insertar_nodo(idx, ciudades, tree, deudas, es_inicial, sig, ant, n_actual):
    pt = ciudades[idx]
    if n_actual > 200:
        _, ids_vecinos = tree.query(pt, k=min(n_actual, 100))
        v1_ids = ids_vecinos[sig[ids_vecinos] != -1]
    else:
        v1_ids = np.where(sig != -1)[0]
    if len(v1_ids) == 0:
        v1_ids = np.where(sig != -1)[0]
    v2_ids = sig[v1_ids]
    v1, v2 = ciudades[v1_ids], ciudades[v2_ids]
    dist_v1_pt = np.sqrt(np.sum((v1 - pt)**2, axis=1))
    dist_pt_v2 = np.sqrt(np.sum((pt - v2)**2, axis=1))
    dist_v1_v2 = np.sqrt(np.sum((v1 - v2)**2, axis=1))
    inc_vec = dist_v1_pt + dist_pt_v2 - dist_v1_v2
    ang_vec = calcular_angulo_vec(v1, pt, v2)
    penalizacion = np.where(ang_vec < 90, (90 - ang_vec)**2 / 50, (180 - ang_vec) / 1000)
    best_idx = np.argmin(inc_vec + penalizacion)
    ganador_v1 = int(v1_ids[best_idx])
    ganador_v2 = int(v2_ids[best_idx])
    sig[ganador_v1] = idx
    ant[idx] = ganador_v1
    sig[idx] = ganador_v2
    ant[ganador_v2] = idx
    if es_inicial: deudas.append(inc_vec[best_idx])
    return idx

def gio_relajacion_local(nodo_centro, ciudades, es_bestia, sig, ant, tree):
    ventana = 6 if es_bestia else 4
    nodos_a_revisar = []
    curr = nodo_centro
    for _ in range(ventana):
        curr = ant[curr]
        nodos_a_revisar.insert(0, curr)
    nodos_a_revisar.append(nodo_centro)
    curr = nodo_centro
    for _ in range(ventana):
        curr = sig[curr]
        nodos_a_revisar.append(curr)
    nodos_a_revisar = list(dict.fromkeys(nodos_a_revisar))
    for p_idx in nodos_a_revisar:
        v_ant = ant[p_idx]
        v_sig = sig[p_idx]
        sig[v_ant] = v_sig
        ant[v_sig] = v_ant
        sig[p_idx] = -1
        ant[p_idx] = -1
        pt_coords = ciudades[p_idx]
        vecinos_topo = [v_ant, v_sig]
        curr_i, curr_d = v_ant, v_sig
        for _ in range(5):
            curr_i = ant[curr_i]
            curr_d = sig[curr_d]
            vecinos_topo.extend([curr_i, curr_d])
        _, ids_geo = tree.query(pt_coords, k=25)
        candidatos_v1 = np.unique(np.concatenate([vecinos_topo, ids_geo]))
        v1_ids = candidatos_v1[sig[candidatos_v1] != -1]
        if len(v1_ids) == 0:
            sig[v_ant] = p_idx
            ant[p_idx] = v_ant
            sig[p_idx] = v_sig
            ant[v_sig] = p_idx
            continue
        v2_ids = sig[v1_ids]
        v1, v2 = ciudades[v1_ids], ciudades[v2_ids]
        dist_v1_p = np.sqrt(np.sum((v1 - pt_coords)**2, axis=1))
        dist_p_v2 = np.sqrt(np.sum((pt_coords - v2)**2, axis=1))
        dist_v1_v2 = np.sqrt(np.sum((v1 - v2)**2, axis=1))
        inc = dist_v1_p + dist_p_v2 - dist_v1_v2
        ang = calcular_angulo_vec(v1, pt_coords, v2)
        energia = inc - (ang / 1000.0)
        best_idx = np.argmin(energia)
        mejor_v1 = int(v1_ids[best_idx])
        mejor_v2 = int(v2_ids[best_idx])
        sig[mejor_v1] = p_idx
        ant[p_idx] = mejor_v1
        sig[p_idx] = mejor_v2
        ant[mejor_v2] = p_idx

def apply_2opt(ruta, ciudades):
    n = len(ruta)
    mejor_ruta = ruta.copy()
    for _ in range(2): 
        cambio_realizado = False
        for i in range(1, n - 2):
            for j in range(i + 1, min(i + 50, n - 1)): 
                A, B = mejor_ruta[i-1], mejor_ruta[i]
                C, D = mejor_ruta[j], mejor_ruta[j+1]
                dist_actual = dist_tsplib(ciudades[A], ciudades[B]) + dist_tsplib(ciudades[C], ciudades[D])
                dist_nueva = dist_tsplib(ciudades[A], ciudades[C]) + dist_tsplib(ciudades[B], ciudades[D])
                if dist_nueva < dist_actual:
                    mejor_ruta[i:j+1] = mejor_ruta[i:j+1][::-1]
                    cambio_realizado = True
        if not cambio_realizado:
            break
    return mejor_ruta

def geometric_insertion_optimizer(ciudades, inicio_idx, tree, centro, es_bestia, cands_ratio):
    n = len(ciudades)
    sig = np.full(n, -1, dtype=int)
    ant = np.full(n, -1, dtype=int)
    sig[inicio_idx] = inicio_idx
    ant[inicio_idx] = inicio_idx
    visitados_mask = np.zeros(n, dtype=bool)
    visitados_mask[inicio_idx] = True
    d_min = np.linalg.norm(ciudades - ciudades[inicio_idx], axis=1)
    deudas = []
    n_actual = 1
    for i in range(n - 1):
        idx = gio_seleccionar_nodo(ciudades, visitados_mask, d_min, inicio_idx, centro, cands_ratio)
        visitados_mask[idx] = True
        pt = ciudades[idx]
        d_min = np.minimum(d_min, np.linalg.norm(ciudades - pt, axis=1))
        nodo_insertado = gio_insertar_nodo(idx, ciudades, tree, deudas, i < 50, sig, ant, n_actual)
        n_actual += 1
        paso_frecuencia = 5 if n > 7000 else 1
        if n_actual > 6 and (i % paso_frecuencia == 0):
            gio_relajacion_local(nodo_insertado, ciudades, es_bestia, sig, ant, tree)
    ruta = []
    curr = inicio_idx
    for _ in range(n):
        ruta.append(int(curr))
        curr = sig[curr]
    ruta_arr = np.array(ruta)
    if n < 50000: 
        ruta_arr = apply_2opt(ruta_arr, ciudades)
    coords_ordenadas = ciudades[ruta_arr]
    siguiente_coords = ciudades[np.roll(ruta_arr, -1)]
    dist_total = int(np.sum(np.floor(np.sqrt(np.sum((coords_ordenadas - siguiente_coords)**2, axis=1)) + 0.5)).item())
    return dist_total

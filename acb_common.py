#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import numpy as np
from sortedcontainers import SortedList

class GIO_CONFIG:
    UMBRAL_KDTREE = 200
    K_VECINOS_INSERCION = 100
    K_VECINOS_RELAJACION = 25
    VENTANA_LOCAL = 4
    MEMORIA_BLOQUE = 10
    INICIO_RELAJACION_LOCAL = 6
    INICIO_RELAJACION_BLOQUE = 15
    FRECUENCIA_BLOQUE = 50
    LIMITE_FASE_INICIAL = 50
    UMBRAL_MAPA_GIGANTE = 7000
    PASO_MAPA_GIGANTE = 5
    ANGULO_AGUDO_MAX = 90
    DIVISOR_PENALIZACION_LEVE = 1000.0
    DIVISOR_DESEMPATE = 1000000.0
    EPSILON = 1e-9

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

def reordenar_por_adn_geometrico(ciudades_canonicas, phi_perturb):
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
        proyeccion_ideal = ((i) * angulo_oro) % 1.0
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

def gio_insertar_nodo(idx, ciudades, tree, deudas, es_inicial, sig, ant, n_actual, nodos_activos):
    pt = ciudades[idx]
    if n_actual > GIO_CONFIG.UMBRAL_KDTREE:
        _, ids_vecinos = tree.query(pt, k=min(n_actual, GIO_CONFIG.K_VECINOS_INSERCION))
        v1_ids = ids_vecinos[sig[ids_vecinos] != -1]
    else:
        activos_arr = np.array(nodos_activos)
        v1_ids = activos_arr[sig[activos_arr] != -1]
    if len(v1_ids) == 0:
        activos_arr = np.array(nodos_activos)
        v1_ids = activos_arr[sig[activos_arr] != -1]
    v2_ids = sig[v1_ids]
    v1, v2 = ciudades[v1_ids], ciudades[v2_ids]
    dist_v1_pt = np.floor(np.sqrt(np.sum((v1 - pt)**2, axis=1)) + 0.5)
    dist_pt_v2 = np.floor(np.sqrt(np.sum((pt - v2)**2, axis=1)) + 0.5)
    dist_v1_v2 = np.floor(np.sqrt(np.sum((v1 - v2)**2, axis=1)) + 0.5)
    inc_vec = dist_v1_pt + dist_pt_v2 - dist_v1_v2
    ang_vec = calcular_angulo_vec(v1, pt, v2)
    penalizacion = np.where(ang_vec < GIO_CONFIG.ANGULO_AGUDO_MAX, (GIO_CONFIG.ANGULO_AGUDO_MAX - ang_vec)**2 / 50, (180 - ang_vec) / GIO_CONFIG.DIVISOR_PENALIZACION_LEVE)
    costo_principal = inc_vec + penalizacion
    criterio_secundario = -ang_vec / GIO_CONFIG.DIVISOR_DESEMPATE
    best_idx = np.argmin(costo_principal + criterio_secundario)
    ganador_v1 = int(v1_ids[best_idx])
    ganador_v2 = int(v2_ids[best_idx])
    sig[ganador_v1] = idx
    ant[idx] = ganador_v1
    sig[idx] = ganador_v2
    ant[ganador_v2] = idx
    if es_inicial: deudas.append(inc_vec[best_idx])
    return idx

def gio_relajacion_bloque(ciudades, indices_objetivo, sig, ant, tree, es_inicial, nodos_activos):
    for idx in indices_objetivo:
        v_ant = ant[idx]
        v_sig = sig[idx]
        if v_ant != -1 and v_sig != -1:
            sig[v_ant] = v_sig
            ant[v_sig] = v_ant
            sig[idx] = -1
            ant[idx] = -1
    for idx in indices_objetivo:
        gio_insertar_nodo(idx, ciudades, tree, [], es_inicial, sig, ant, len(ciudades), nodos_activos)

def gio_relajacion_local(nodo_centro, ciudades, sig, ant, tree):
    ventana = GIO_CONFIG.VENTANA_LOCAL
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
        _, ids_geo = tree.query(pt_coords, k=GIO_CONFIG.K_VECINOS_RELAJACION)
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
        dist_v1_p = np.floor(np.sqrt(np.sum((v1 - pt_coords)**2, axis=1)) + 0.5)
        dist_p_v2 = np.floor(np.sqrt(np.sum((pt_coords - v2)**2, axis=1)) + 0.5)
        dist_v1_v2 = np.floor(np.sqrt(np.sum((v1 - v2)**2, axis=1)) + 0.5)
        inc = dist_v1_p + dist_p_v2 - dist_v1_v2
        ang = calcular_angulo_vec(v1, pt_coords, v2)
        energia = inc - (ang / GIO_CONFIG.DIVISOR_PENALIZACION_LEVE)
        desempate = -ang / GIO_CONFIG.DIVISOR_DESEMPATE
        best_idx = np.argmin(energia + desempate)
        mejor_v1 = int(v1_ids[best_idx])
        mejor_v2 = int(v2_ids[best_idx])
        sig[mejor_v1] = p_idx
        ant[p_idx] = mejor_v1
        sig[p_idx] = mejor_v2
        ant[mejor_v2] = p_idx

def geometric_insertion_optimizer(ciudades, inicio_idx, tree, centro, cands_ratio):
    n = len(ciudades)
    sig = np.full(n, -1, dtype=int)
    ant = np.full(n, -1, dtype=int)
    sig[inicio_idx] = inicio_idx
    ant[inicio_idx] = inicio_idx
    visitados_mask = np.zeros(n, dtype=bool)
    visitados_mask[inicio_idx] = True
    d_min = np.floor(np.linalg.norm(ciudades - ciudades[inicio_idx], axis=1) + 0.5)
    deudas = []
    n_actual = 1
    ultimas_insertadas = []
    nodos_activos = [inicio_idx] 
    for i in range(n - 1):
        idx = gio_seleccionar_nodo(ciudades, visitados_mask, d_min, inicio_idx, centro, cands_ratio)
        visitados_mask[idx] = True
        ultimas_insertadas.append(idx)
        if len(ultimas_insertadas) > GIO_CONFIG.MEMORIA_BLOQUE:
            ultimas_insertadas.pop(0)
        pt = ciudades[idx]
        dist_a_pt = np.floor(np.linalg.norm(ciudades - pt, axis=1) + 0.5)
        d_min = np.minimum(d_min, dist_a_pt)
        nodo_insertado = gio_insertar_nodo(idx, ciudades, tree, deudas, i < GIO_CONFIG.LIMITE_FASE_INICIAL, sig, ant, n_actual, nodos_activos)
        nodos_activos.append(idx) 
        n_actual += 1
        paso_frecuencia = GIO_CONFIG.PASO_MAPA_GIGANTE if n > GIO_CONFIG.UMBRAL_MAPA_GIGANTE else 1
        if n_actual > GIO_CONFIG.INICIO_RELAJACION_LOCAL and (i % paso_frecuencia == 0):
            gio_relajacion_local(nodo_insertado, ciudades, sig, ant, tree)
        if n_actual > GIO_CONFIG.INICIO_RELAJACION_BLOQUE and n_actual % GIO_CONFIG.FRECUENCIA_BLOQUE == 0:
            gio_relajacion_bloque(ciudades, ultimas_insertadas, sig, ant, tree, i < GIO_CONFIG.LIMITE_FASE_INICIAL, nodos_activos)
    ruta = []
    curr = inicio_idx
    for _ in range(n):
        ruta.append(int(curr))
        curr = sig[curr]
    ruta_arr = np.array(ruta)
    coords_ordenadas = ciudades[ruta_arr]
    siguiente_coords = ciudades[np.roll(ruta_arr, -1)]
    dist_total = int(np.sum(np.floor(np.sqrt(np.sum((coords_ordenadas - siguiente_coords)**2, axis=1)) + 0.5)).item())
    return ruta_arr.tolist(), dist_total

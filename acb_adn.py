#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import numpy as np
from scipy.spatial import KDTree
from acb_common import reordenar_por_adn_geometrico, calcular_angulo_vec, calcular_candidato_adn, geometric_insertion_optimizer

def acb_adn(ciudades_input):
    indices_canonicos = np.lexsort((ciudades_input[:, 1], ciudades_input[:, 0]))
    ciudades_canonicas = ciudades_input[indices_canonicos]
    centro = np.mean(ciudades_canonicas, axis=0)
    off_inf, phi_inf, ratio_inf = 0, 0.05, 0.8
    ciudades = reordenar_por_adn_geometrico(ciudades_canonicas, offset=off_inf, phi_perturb=phi_inf)
    n_nodos = len(ciudades)
    centro = np.mean(ciudades, axis=0)
    tree = KDTree(ciudades)
    dist_centro = np.linalg.norm(ciudades - centro, axis=1)
    _, ids_cercanos = tree.query(ciudades, k=3)
    v1, v2 = ciudades[ids_cercanos[:, 1]], ciudades[ids_cercanos[:, 2]]
    angulos_locales = calcular_angulo_vec(v1, ciudades, v2)
    dist_k, _ = tree.query(ciudades, k=11)
    proximidad_relativa = dist_k[:, 1] / (np.mean(dist_k[:, 1:], axis=1) + 1e-6)
    vec_cands = ciudades - centro
    angs_cands = np.degrees(np.arctan2(vec_cands[:, 1], vec_cands[:, 0]))
    diff_angs_cands = (np.diff(angs_cands) + 180) % 360 - 180
    var_ang_cands = np.var(diff_angs_cands)
    candidate_scores = calcular_candidato_adn(dist_centro, angulos_locales, proximidad_relativa, var_ang_cands)
    candidatos_priorizados = sorted(candidate_scores, key=candidate_scores.get, reverse=True)[:1]
    resultados = [geometric_insertion_optimizer(ciudades, i, tree, centro, n_nodos > 5000, ratio_inf) for i in candidatos_priorizados]
    mejor_distancia = min(resultados)
    dist = mejor_distancia
    return dist
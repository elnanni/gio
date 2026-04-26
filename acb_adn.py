#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import numpy as np
from scipy.spatial import KDTree
from acb_common import reordenar_por_adn_geometrico, geometric_insertion_optimizer

def acb_adn(ciudades_input, mapa, optimo_real):
    np.set_printoptions(
        precision=1,
        suppress=True,
        threshold=np.inf,
        linewidth=120
    )
    indices_canonicos = np.lexsort((ciudades_input[:, 1], ciudades_input[:, 0]))
    ciudades_canonicas = ciudades_input[indices_canonicos]
    centro = np.mean(ciudades_canonicas, axis=0)
    n_nodos = len(ciudades_canonicas)
    phis_a_probar = np.linspace(0.05, 0.1, 360)
    ratios_a_probar = np.linspace(0.1, 0.99, 357)
    nodos_a_probar = list(range(0, n_nodos, 1))
    mejor_distancia_global = float('inf')
    for p_test in phis_a_probar:
        ciudades_adn = reordenar_por_adn_geometrico(ciudades_canonicas, phi_perturb=p_test)
        tree = KDTree(ciudades_adn)
        for r_test in ratios_a_probar:
            resultados = [geometric_insertion_optimizer(ciudades_adn, i, tree, centro, r_test) for i in nodos_a_probar]
            for _, (_, dist_bloque) in zip(nodos_a_probar, resultados):
                if dist_bloque < mejor_distancia_global:
                    mejor_distancia_global = dist_bloque
    return mejor_distancia_global

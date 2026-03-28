#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import time
import os
from acb_adn import acb_adn
from lector import cargar_tsplib

def ejecutar_world_tour(archivo_tsp, optimo_real):
    nombre_base = os.path.basename(archivo_tsp).replace(".tsp", "")
    ciudades = cargar_tsplib(archivo_tsp)
    if ciudades is None or len(ciudades) == 0:
        return
    t0 = time.perf_counter()
    dist_acb = acb_adn(ciudades)
    tiempo_acb = time.perf_counter() - t0
    gap = ((dist_acb / optimo_real) - 1) * 100
    print(f"\nEnd {nombre_base}: Gap {gap:.4f}% in {tiempo_acb:.4f}s. Distance {dist_acb}")

if __name__ == "__main__":
    ejecutar_world_tour("ejercicios/pruebaia.tsp", 360.0)
    #ejecutar_world_tour("ejercicios/wi29.tsp", 27603.0)
    #ejecutar_world_tour("ejercicios/dj38.tsp", 6656.0)
    #ejecutar_world_tour("ejercicios/eil51.tsp", 426)
    #ejecutar_world_tour("ejercicios/berlin52.tsp", 7542)
    #ejecutar_world_tour("ejercicios/st70.tsp", 675)
    #ejecutar_world_tour("ejercicios/eil76.tsp", 538)
    #ejecutar_world_tour("ejercicios/rat99.tsp", 1211)
    #ejecutar_world_tour("ejercicios/kroA100.tsp", 21282)
    #ejecutar_world_tour("ejercicios/kroB100.tsp", 22141)
    #ejecutar_world_tour("ejercicios/kroC100.tsp", 20749)
    #ejecutar_world_tour("ejercicios/kroD100.tsp", 21294)
    #ejecutar_world_tour("ejercicios/kroE100.tsp", 22068)
    #ejecutar_world_tour("ejercicios/rd100.tsp", 7910)
    #ejecutar_world_tour("ejercicios/xqf131.tsp", 564.0)
    #ejecutar_world_tour("ejercicios/qa194.tsp", 9352.0)
    #ejecutar_world_tour("ejercicios/xqg237.tsp", 1019.0)
    #ejecutar_world_tour("ejercicios/pma343.tsp", 1368.0)
    #ejecutar_world_tour("ejercicios/pka379.tsp", 1332.0)
    #ejecutar_world_tour("ejercicios/pbk411.tsp", 1343.0)
    #ejecutar_world_tour("ejercicios/xql662.tsp", 2513.0)
    #ejecutar_world_tour("ejercicios/rbx711.tsp", 3115.0)
    #ejecutar_world_tour("ejercicios/uy734.tsp", 79114.0)
    #ejecutar_world_tour("ejercicios/zi929.tsp", 95103.0)
    #ejecutar_world_tour("ejercicios/lu980.tsp", 11340.0)
    #ejecutar_world_tour("ejercicios/rw1621.tsp", 26051.0)
    #ejecutar_world_tour("ejercicios/mu1979.tsp", 86891.0)
    #ejecutar_world_tour("ejercicios/nu3496.tsp", 96132.0)
    #ejecutar_world_tour("ejercicios/ca4663.tsp", 1290319.0)
    #ejecutar_world_tour("ejercicios/tz6117.tsp", 394718.0)
    #ejecutar_world_tour("ejercicios/eg7146.tsp", 172350.0)
    #ejecutar_world_tour("ejercicios/ar9152.tsp", 837377.0)
    #ejecutar_world_tour("ejercicios/fi10639.tsp", 520527.0)
    #ejecutar_world_tour("ejercicios/bm33708.tsp", 959304.0)

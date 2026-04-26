#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import time
import os
import csv
from acb_adn import acb_adn
from lector import cargar_tsplib

resultados_tour = []

def ejecutar_world_tour(archivo_tsp, optimo_real):
    nombre_base = os.path.basename(archivo_tsp).replace(".tsp", "")
    ciudades = cargar_tsplib(archivo_tsp)
    if ciudades is None or len(ciudades) == 0:
        return
    t0 = time.perf_counter()
    dist_acb = acb_adn(ciudades, nombre_base, optimo_real)
    tiempo_acb = time.perf_counter() - t0
    gap = ((dist_acb / optimo_real) - 1) * 100
    resultados_tour.append({"Mapa": nombre_base, "Nodos": len(ciudades), "Optimo": optimo_real, "GIO": dist_acb, "Gap": f"{gap:.4f}%", "Tiempo": f"{tiempo_acb:.2f}s"})
    print(f"\nEnd {nombre_base}: Gap {gap:.4f}% in {tiempo_acb:.4f}s. Distance {dist_acb}")

def guardar_reporte_final():
    os.makedirs("resultados", exist_ok=True)
    with open("resultados/tabla_final.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=resultados_tour[0].keys())
        writer.writeheader()
        writer.writerows(resultados_tour)

if __name__ == "__main__":
    ejecutar_world_tour("ejercicios/wi29.tsp", 27603.0)
    ejecutar_world_tour("ejercicios/ia36.tsp", 360.0)
    ejecutar_world_tour("ejercicios/dj38.tsp", 6656.0)
    ejecutar_world_tour("ejercicios/iadb40.tsp", 680.0)
    ejecutar_world_tour("ejercicios/jb_caos_cv205_4f2_50.tsp", 3217)
    ejecutar_world_tour("ejercicios/jb_caos_cv148_1a6_50.tsp", 4123)
    ejecutar_world_tour("ejercicios/eil51.tsp", 426)
    ejecutar_world_tour("ejercicios/iatdb52.tsp", 722)
    ejecutar_world_tour("ejercicios/berlin52.tsp", 7542)
    ejecutar_world_tour("ejercicios/iatr60.tsp", 3090)
    ejecutar_world_tour("ejercicios/st70.tsp", 675)
    ejecutar_world_tour("ejercicios/eil76.tsp", 538)
    ejecutar_world_tour("ejercicios/pr76.tsp", 108159)
    ejecutar_world_tour("ejercicios/rat99.tsp", 1211)
    ejecutar_world_tour("ejercicios/jb_caos_cv194_916_100.tsp", 3991)
    ejecutar_world_tour("ejercicios/jb_alea_cv64_ce0_100.tsp", 8056)
    ejecutar_world_tour("ejercicios/jb_caos_cv135_c0c_100.tsp", 5734)
    ejecutar_world_tour("ejercicios/iasnake100.tsp", 1720)
    ejecutar_world_tour("ejercicios/kroA100.tsp", 21282)
    ejecutar_world_tour("ejercicios/kroB100.tsp", 22141)
    ejecutar_world_tour("ejercicios/kroC100.tsp", 20749)
    ejecutar_world_tour("ejercicios/kroD100.tsp", 21294)
    ejecutar_world_tour("ejercicios/kroE100.tsp", 22068)
    ejecutar_world_tour("ejercicios/rd100.tsp", 7910)
    ejecutar_world_tour("ejercicios/eil101.tsp", 629)
    ejecutar_world_tour("ejercicios/lin105.tsp", 14379)
    ejecutar_world_tour("ejercicios/pr107.tsp", 44303)
    ejecutar_world_tour("ejercicios/bier127.tsp", 118282)
    ejecutar_world_tour("ejercicios/ch130.tsp", 6110)
    ejecutar_world_tour("ejercicios/xqf131.tsp", 564.0)
    ejecutar_world_tour("ejercicios/jb_alea_cv58_e65_150.tsp", 9107)
    ejecutar_world_tour("ejercicios/jb_caos_cv108_400_150.tsp", 7708)
    ejecutar_world_tour("ejercicios/jb_caos_cv131_247_150.tsp", 7173)
    ejecutar_world_tour("ejercicios/jb_caos_cv254_c91_150.tsp", 5031)
    ejecutar_world_tour("ejercicios/ch150.tsp", 6528)
    ejecutar_world_tour("ejercicios/kroB150.tsp", 26130)
    ejecutar_world_tour("ejercicios/u159.tsp", 42080)
    ejecutar_world_tour("ejercicios/qa194.tsp", 9352.0)
    ejecutar_world_tour("ejercicios/d198.tsp", 15780.0)
    ejecutar_world_tour("ejercicios/jb_caos_cv265_cef_200.tsp", 5437)
    ejecutar_world_tour("ejercicios/tsp225.tsp", 3916.0)
    ejecutar_world_tour("ejercicios/ts225.tsp", 126643.0)
    ejecutar_world_tour("ejercicios/xqg237.tsp", 1019.0)
    ejecutar_world_tour("ejercicios/a280.tsp", 2579.0)
    ejecutar_world_tour("ejercicios/pma343.tsp", 1368.0)
    ejecutar_world_tour("ejercicios/pka379.tsp", 1332.0)
    ejecutar_world_tour("ejercicios/pbk411.tsp", 1343.0)
    ejecutar_world_tour("ejercicios/fl417.tsp", 11861.0)
    ejecutar_world_tour("ejercicios/pcb442.tsp", 50778.0)
    ejecutar_world_tour("ejercicios/xql662.tsp", 2513.0)
    ejecutar_world_tour("ejercicios/rbx711.tsp", 3115.0)
    ejecutar_world_tour("ejercicios/uy734.tsp", 79114.0)
    ejecutar_world_tour("ejercicios/zi929.tsp", 95103.0)
    ejecutar_world_tour("ejercicios/lu980.tsp", 11340.0)
    ejecutar_world_tour("ejercicios/rw1621.tsp", 26051.0)
    ejecutar_world_tour("ejercicios/mu1979.tsp", 86891.0)
    ejecutar_world_tour("ejercicios/nu3496.tsp", 96132.0)
    ejecutar_world_tour("ejercicios/ca4663.tsp", 1290319.0)
    ejecutar_world_tour("ejercicios/tz6117.tsp", 394718.0)
    ejecutar_world_tour("ejercicios/eg7146.tsp", 172350.0)
    ejecutar_world_tour("ejercicios/ar9152.tsp", 837377.0)
    ejecutar_world_tour("ejercicios/fi10639.tsp", 520527.0)
    ejecutar_world_tour("ejercicios/bm33708.tsp", 959304.0)
    guardar_reporte_final()

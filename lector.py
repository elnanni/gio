#  Copyright (C) 2026  jbenavides
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
import numpy as np

def cargar_tsplib(ruta_archivo):
    coords = []
    try:
        with open(ruta_archivo, 'r') as f:
            lineas = f.readlines()
            in_section = False
            for linea in lineas:
                linea = linea.strip()
                if "NODE_COORD_SECTION" in linea:
                    in_section = True
                    continue
                if not in_section:
                    continue
                if "EOF" in linea:
                    break
                if not linea:
                    continue
                partes = linea.split()
                if len(partes) >= 3:
                    try:
                        coords.append([float(partes[1]), float(partes[2])])
                    except ValueError:
                        continue
    except Exception as e:
        print(f"[ERROR] No such file {ruta_archivo}: {e}")
    res = np.array(coords)
    return res

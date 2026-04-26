# 🚀 GIO & ACB: TSP Solver (Geometric Insertion Optimizer)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python: 3.7+](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)

## 📌 Descripción

Este proyecto presenta una implementación de alto rendimiento para resolver el **Problema del Viajante de Comercio (TSP)**. Utiliza una combinación de **ordenación geométrica inspirada en ADN**, **inserción geométrica adaptativa** y **relajación topológica** para construir rutas de alta calidad.

El flujo principal del motor es:

1. Cargar coordenadas TSPLIB desde `lector.py`.
2. Reordenar las ciudades usando una perturbación del ángulo dorado en `acb_adn.py`.
3. Explorar una alta resolución de parámetros (`phis` y `ratios`) para validar la Resonancia Geométrica del ADN.
4. Evaluar rutas desde cada nodo inicial y refinar la topología con inserciones angulares y relajaciones locales/bloque.

A diferencia de las heurísticas clásicas de "Vecino más Cercano", este motor prioriza la topología global y evita cruces prematuros desde la fase constructiva.

> ⚠️ AVISO: La configuración actual utiliza una búsqueda en malla de alta resolución (360 Phis x 357 Ratios x nodos iniciales). Esto está pensado para la validación científica de la Resonancia Geométrica del ADN. Para aproximaciones rápidas en mapas grandes, reduce la resolución de `np.linspace(...)` en `acb_adn.py`.

---

## 🧠 Arquitectura del Motor

El solver se apoya en tres componentes clave:

### 1. Ordenación geométrica tipo ADN

La función `reordenar_por_adn_geometrico` genera una permutación inicial de ciudades basada en un perturbador del ángulo dorado. Esta ordenación establece una base estructurada para la construcción de la ruta.

### 2. Inserción Geométrica Optimizada (GIO)

El núcleo de `acb_common.py` ejecuta la inserción de nodos siguiendo estos principios:

- **Selección de candidatos basada en distancia y dirección.**
- **KDTree para vecinos cercanos.**
- **Penalización de ángulos agudos** para favorecer inserciones más suaves.
- **Relajación local y por bloques** que corrige la topología tras cada expansión de la ruta.

### 3. Evaluación y experimentación TSPLIB

El módulo `evaluador.py` recorre instancias `.tsp`, ejecuta el solver y guarda los resultados en `resultados/tabla_final.csv`. Esto permite comparar el rendimiento en múltiples mapas y optimizar parámetros.

---

## ✅ Licencia

Este proyecto está bajo la licencia **GNU GPL v3**.

> "La libertad de usar, estudiar, compartir y modificar el software."

Cualquier trabajo derivado de este motor debe mantener la misma licencia y compartir sus mejoras con la comunidad.

This project is licensed under the AGPLv3. If you wish to use GIO in a private commercial environment or without open-sourcing your code, you can request a commercial license by contacting: [elnanni@gmail.com](mailto:elnanni@gmail.com)

Este proyecto está bajo la licencia AGPLv3. Si deseas utilizar GIO en un entorno comercial privado o sin abrir tu código fuente, puedes solicitar una licencia comercial escribiendo a: [elnanni@gmail.com](mailto:elnanni@gmail.com)

**Copyright (C) 2026 jbenavides**

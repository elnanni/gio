# 🚀 GIO & ACB: TSP Solver (Geometric Insertion Optimizer)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python: 3.7+](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)

## 📌 Descripción

Este proyecto presenta una implementación de alto rendimiento para resolver el **Problema del Viajante de Comercio (TSP)**. Utiliza una arquitectura híbrida que combina **Inserción Geométrica Adaptativa** con un **Escaneo de Horizonte** basado en proyecciones vectoriales.

A diferencia de las heurísticas clásicas de "Vecino más Cercano", este motor prioriza la estructura global del mapa para evitar cruces prematuros y optimizar la topología de la ruta desde el primer nodo.

---

## 🧠 Arquitectura del Motor

El solver se divide en tres capas lógicas diseñadas para maximizar la precisión sin sacrificar la velocidad:

### 1. Algoritmo GIO (Geometric Insertion Optimizer)

Es el núcleo de construcción de la ruta, caracterizado por:

- **Criterio de Inserción Suave:** Al insertar un nodo, el algoritmo no solo busca la distancia mínima, sino que penaliza ángulos agudos que puedan generar rutas "quebradas".
- **KD-Tree Integration:** Uso de estructuras de datos espaciales para búsquedas de proximidad en O(log n).
- **Relajación Local Híbrida:** Un proceso de refinamiento en caliente que re-evalúa la posición de los nodos recién insertados para corregir decisiones subóptimas de la fase constructiva.

### 2. Refinamiento 2-opt Light

Como paso final, se aplica un algoritmo **2-opt optimizado** con ventana local. Este proceso detecta y elimina cruces de líneas ("X"), "planchando" la ruta final para mejorar el costo sin disparar el tiempo de cómputo.

---

## ✅ Licencia

Este proyecto está bajo la licencia **GNU GPL v3**.

> "La libertad de usar, estudiar, compartir y modificar el software."

Cualquier trabajo derivado de este motor debe mantener la misma licencia y compartir sus mejoras con la comunidad.

**Copyright (C) 2026 jbenavides**

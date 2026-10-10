---
title: Polysome
descripcion: Un motor de inferencia escrito desde cero en C++ y CUDA para la familia GPT 2, con el objetivo de generar proteínas con ProtGPT2 lo más rápido posible en una RTX 2060 Super.
repo: https://github.com/gpylypchuk/polysome
estado: En curso, hito M00
orden: 1
---

## Objetivo

El objetivo es generar secuencias de proteína con ProtGPT2 con el mayor throughput posible
en una RTX 2060 Super. ProtGPT2 es un modelo de 738 millones de parámetros con la
arquitectura de GPT 2, entrenado con secuencias de proteínas en lugar de
texto.{% sidenote 'sn-protgpt2' 'Ferruz, Schmidt y Höcker (2022), *ProtGPT2 is a deep unsupervised language model for protein design*, Nature Communications.' %}
La referencia de comparación es el `generate` de HuggingFace, y la distribución de salida
tiene que ser la misma. Una mejora de velocidad que cambie lo que el modelo genera no
cuenta.

El proyecto demuestra infraestructura y no biología. Validar que una secuencia generada
sirve como proteína requiere predicción de estructura y pruebas de laboratorio, y eso
queda fuera del alcance.

## Hoja de ruta

El proyecto se divide en hitos, y cada uno deja algo que funciona y se puede medir antes
de pasar al siguiente.

- **M00** Preparación y datos de referencia
- **M01** Forward en CPU, validado contra PyTorch
- **M02** Primeros kernels de CUDA
- **M03** Multiplicación de matrices rápida
- **M04** Atención y fusión de kernels
- **M05** Muestreo para ProtGPT2
- **M06** Precisión reducida, fp16 e int8
- **M07** Batching continuo, el resultado principal
- **M08** Opcional, puntuar secuencias con ESM 2

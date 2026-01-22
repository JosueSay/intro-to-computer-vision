# Laboratorio 1

## Task 3 – Evaluación de Ingenería y Criterio

En esta parte se evaluará la aplicación de sus algoritmos en situaciones reales. Use imágenes propias o descargue un dataset de “suelos de almacén” o “carreteras con textura”.

### Experimento A: El efecto de Sigma ($\sigma$)

Cargue una imagen con ruido (agregue ruido "Sal y Pimienta" o Gaussiano artificialmente a una foto limpia si es necesario).

1. Genere 3 versiones de detección de bordes (Magnitud Sobel) variando el pre-procesamiento Gaussiano:
   - a. Sin suavizado.
   - b. Gaussiano $\sigma = 1$ (kernel sugerido 5x5).
   - c. Gaussiano $\sigma = 5$ (kernel sugerido 31x31).

2. **Análisis:** Muestre las tres imágenes de bordes resultantes. ¿Qué pasa con los bordes finos cuando $\sigma$ es muy alto? ¿Qué pasa con la textura del suelo cuando no hay suavizado? Como ingeniero, ¿cuál elegiría para detectar pallets grandes ignorando grietas pequeñas en el suelo?

### Experimento B: Histéresis Manual (Simulación de Canny)

Usted ha calculado la Magnitud del Gradiente en el paso 3.3. Ahora implemente una función simple de umbralización `umbral_simple(magnitud, T)` y compare visualmente con `cv2.Canny`.

1. Intente encontrar un valor $T$ único que limpie el ruido pero mantenga los bordes.
2. Observe el resultado: ¿Se rompen las líneas de los bordes?
3. **Pregunta Crítica:** Explique por qué un simple umbral de corte (Thresholding) nunca será tan efectivo como el método de Histéresis usado en Canny. ¿Qué problema específico resuelve la conectividad de la histéresis en el contexto de un robot moviéndose y vibrando (lo que causa cambios leves de iluminación en los bordes)?

# Laboratorio 1

## Task 3 – Evaluación de Ingenería y Criterio

En esta parte se evaluará la aplicación de sus algoritmos en situaciones reales. Use imágenes propias o descargue un dataset de “suelos de almacén” o “carreteras con textura”.

### Experimento A: El efecto de Sigma ($\sigma$)

Cargue una imagen con ruido (agregue ruido "Sal y Pimienta" o Gaussiano artificialmente a una foto limpia si es necesario).

#### Inciso 1

Genere 3 versiones de detección de bordes (Magnitud Sobel) variando el pre-procesamiento Gaussiano:

- a. Sin suavizado.
- b. Gaussiano $\sigma = 1$ (kernel sugerido 5x5).
- c. Gaussiano $\sigma = 5$ (kernel sugerido 31x31).

Se aplicó el operador Sobel sobre la imagen ruidosa en tres escenarios. En los casos (b) y (c), la imagen fue preprocesada con un **filtro Gaussiano** generado manualmente (Task 2) antes de calcular el gradiente.
En todos los casos, la magnitud del gradiente se calculó como:

$$
G = \sqrt{G_x^2 + G_y^2}
$$

y se normalizó a 0–255 para visualización.

#### Inciso 2

Muestre las tres imágenes de bordes resultantes. ¿Qué pasa con los bordes finos cuando $\sigma$ es muy alto? ¿Qué pasa con la textura del suelo cuando no hay suavizado? Como ingeniero, ¿cuál elegiría para detectar pallets grandes ignorando grietas pequeñas en el suelo?

- **Sin suavizado:**
  El mapa de bordes presenta una gran cantidad de respuestas espurias. La textura del ruido genera muchos gradientes locales, produciendo un resultado muy cargado y poco útil. Se detectan tanto bordes reales como variaciones pequeñas debidas al ruido.

- **Gaussiano con $\sigma = 1$:**
  El suavizado elimina parte del ruido de alta frecuencia sin borrar completamente los bordes relevantes. El resultado es un mapa de bordes más limpio, donde las estructuras principales permanecen visibles, aunque aún se conservan algunos detalles finos.

- **Gaussiano con $\sigma = 5$:**
  El suavizado es mucho más agresivo. Los **bordes finos desaparecen** casi por completo y solo permanecen las estructuras grandes y continuas. La textura del suelo se atenúa significativamente, pero también se pierde precisión en la localización exacta de los bordes.

Cuando $\sigma$ es muy alto, los bordes finos se eliminan junto con el ruido, lo que reduce la sensibilidad del detector a pequeñas variaciones.
Cuando no hay suavizado, la textura del suelo y el ruido generan demasiados falsos bordes, dificultando cualquier decisión posterior.

Para detectar pallets grandes e ignorar grietas pequeñas del suelo, la opción más adecuada es un **suavizado Gaussiano con $\sigma$ alto** (por ejemplo $\sigma = 5$). Aunque se pierde detalle fino, se obtiene un mapa de bordes más estable y robusto.

![Resultado Experimento A](../images/task3.result-image-expA.png)

### Experimento B: Histéresis Manual (Simulación de Canny)

Usted ha calculado la Magnitud del Gradiente en el paso 3.3. Ahora implemente una función simple de umbralización `umbral_simple(magnitud, T)` y compare visualmente con `cv2.Canny`.

1. Intente encontrar un valor $T$ único que limpie el ruido pero mantenga los bordes.
2. Observe el resultado: ¿Se rompen las líneas de los bordes?
3. **Pregunta Crítica:** Explique por qué un simple umbral de corte (Thresholding) nunca será tan efectivo como el método de Histéresis usado en Canny. ¿Qué problema específico resuelve la conectividad de la histéresis en el contexto de un robot moviéndose y vibrando (lo que causa cambios leves de iluminación en los bordes)?

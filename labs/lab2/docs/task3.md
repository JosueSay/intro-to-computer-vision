# Laboratorio 1

## Task 3 – Evaluación de Ingenería y Criterio

Una fábrica textil necesita detectar rasgaduras en telas de mezclilla (denim) automáticamente. El problema es que la tela tiene una textura natural fuerte (patrón repetitivo) que confunde a los detectores de bordes simples (Canny), detectando el tejido como si fuera un defecto. Por ello se le pide que usted diseñe un pipeline híbrido que combine Fourier y Morfología para aislar solamente la rasgadura. Para ello comienza por probar su solución en una imagen que tiene a mano.

Para esta parte se espera que su entregable muestre

- Implementación del Pipeline completo (FFT -> Filtro -> IFFT -> Threshold -> Morfología).
- Resultado final: Una máscara binaria donde el fondo sea negro y la rasgadura sea blanca, sin falsos positivos de la textura de la tela.
- Escriba un párrafo (aprox. 100 palabras) describiendo los trade-offs de su solución. ¿Qué pasa si la rasgadura es muy pequeña? ¿Qué pasa si cambiamos el tipo de tela? ¿Es su solución robusta o específica para esta imagen?

### Inciso 1

Utilice Fourier para analizar la textura repetitiva de la tela. Diseñe un filtro que elimine las frecuencias altas/repetitivas del tejido, dejando una imagen "suavizada" donde solo resalte la anomalía (la rasgadura) y la iluminación global. (Supresión de Textura)

   1. Hint: ¿Qué pasa si eliminamos las frecuencias altas periféricas o específicas?

### Inciso 2

Aplique un umbralizado (thresholding) a la imagen resultante del paso 1 para obtener una máscara binaria preliminar. (Segmentación)

### Inciso 3

La máscara seguramente tendrá ruido residual. Utilice operaciones morfológicas para limpiar la máscara y dejar únicamente la silueta de la rasgadura. (Refinamiento)

# Laboratorio 2

## Task 3

Una fábrica textil necesita detectar rasgaduras en telas de mezclilla (denim) automáticamente. El problema es que la tela tiene una textura natural fuerte (patrón repetitivo) que confunde a los detectores de bordes simples (Canny), detectando el tejido como si fuera un defecto. Por ello se le pide que usted diseñe un pipeline híbrido que combine Fourier y Morfología para aislar solamente la rasgadura. Para ello comienza por probar su solución en una imagen que tiene a mano.

### Estrategia

Se implementó un pipeline híbrido **FFT → Filtro → IFFT → Threshold → Morfología** para suprimir la textura periódica del denim y aislar la rasgadura como una anomalía no repetitiva.

#### Inciso 1. Supresión de textura con Fourier

La imagen se analizó en el dominio de la frecuencia mediante FFT, observando que la textura del tejido se manifiesta como componentes repetitivas en altas frecuencias (zonas periféricas del espectro). Para atenuarlas se aplicó un **filtro pasa-bajo circular centrado**, conservando principalmente las bajas frecuencias asociadas a iluminación global y estructuras grandes. Luego se reconstruyó la imagen suavizada con IFFT, reduciendo drásticamente el patrón del tejido y manteniendo la rasgadura como variación destacable.

#### Inciso 2. Segmentación por umbralizado

Sobre la imagen reconstruida (suavizada), se aplicó un **umbral binario** para obtener una máscara preliminar. Esto separa regiones anómalas (rasgadura) del fondo, aprovechando que la textura ya fue suprimida en el paso anterior.

#### Inciso 3. Refinamiento morfológico

La máscara inicial aún puede contener ruido residual. Para limpiarla se aplicó una secuencia morfológica de **apertura** (elimina puntos/fragmentos pequeños) seguida de **cierre** (conecta discontinuidades y rellena pequeños huecos), obteniendo finalmente una **máscara binaria** con fondo negro y la rasgadura en blanco, minimizando falsos positivos de la textura.

### Trade-offs

La solución es efectiva cuando la textura del denim es periódica y la rasgadura tiene una forma/escala distinta al patrón. El principal trade-off es que un filtro pasa-bajo puede suavizar tanto la imagen que una rasgadura muy pequeña o delgada se atenúe y se pierda durante el thresholding o sea eliminada por la apertura. Además, si cambia el tipo de tela (otro patrón, distinta periodicidad o texturas no tan regulares), el filtro en frecuencia puede dejar pasar componentes del tejido o eliminar rasgos del defecto. Por ello, el método requiere ajustar el filtro y la morfología según la textura.

![Pipeline](../images/task3.result1.png)

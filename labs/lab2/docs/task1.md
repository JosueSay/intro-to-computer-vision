# Laboratorio 2

## Task 1

Usted trabaja para una empresa de imágenes satelitales. Una de las cámaras en órbita tiene una interferencia electrónica que genera un ruido sinusoidal (patrón de rayas diagonales) sobre las fotografías de la superficie terrestre. Los filtros espaciales tradicionales (Gaussian Blur) destruyen los detalles geográficos necesarios. Por ello usted ha decidido idear una solución tomando como base fotografías que tiene a mano con el mismo problema previo a implementar la solución real. Con esto en mente, realice:

Para esta parte se espera que entregue:

- Código funcional y visualización correcta del espectro con los picos de ruidos señalados
- Imagen restaurada exitosamente (sin rayas y con detalles nítidos)
- Explique por qué un filtro de promedio (average filter) de 5x5 en el dominio espacial hubiera sido una mala solución para este problema específico.

### Inciso 1

Cargue la imagen `periodic_noise.jpg` en escala de grises.
<!-- 
![Imagen original con ruido periódico](../images/periodic_noise.jpg) -->

### Inciso 2

Calcule la Transformada Discreta de Fourier (DFT) y desplace el componente de frecuencia cero al centro.

![DFT centrada](../images/task1_dft_centered.png)

### Inciso 3

Muestre el Espectro de Magnitud en escala logarítmica.

![Espectro de magnitud en escala logarítmica](../images/task1_magnitude_spectrum.png)

### Inciso 4

Identifique visualmente los "picos" de energía que no corresponden a la información natural de la imagen (puntos brillantes fuera del centro).

En el espectro se observan picos brillantes simétricos alejados del centro, los cuales corresponden al ruido sinusoidal periódico responsable de las rayas diagonales en la imagen original.

![Picos de ruido señalados](../images/task1_magnitude_peaks.png)

### Inciso 5

Cree una máscara (Notch Filter) que bloquee específicamente esas frecuencias parásitas (haciéndolas cero), pero preserve el resto del espectro, incluyendo el componente DC.

![Máscara Notch Filter](../images/task1_notch_mask.png)

### Inciso 6

Aplique la Transformada Inversa (IDFT) para recuperar la imagen espacial.

![Imagen restaurada sin ruido periódico](../images/task1_restored.png)

### Justificación del método

Un filtro de promedio (average filter) de 5×5 en el dominio espacial hubiera sido una mala solución para este problema porque actúa como un suavizador global. Aunque reduce ruido, también degrada bordes, texturas y detalles geográficos importantes. Dado que el ruido es periódico y se concentra en frecuencias específicas del dominio de Fourier, el uso de un Notch Filter permite eliminar selectivamente dichas frecuencias sin afectar significativamente la información útil de la imagen.

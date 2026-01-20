# Hoja de Trabajo 1

## Task 2 – Práctica

Su objetivo es implementar un pipeline de pre-procesamiento manual, manipulando tensores y gestionando tipos de datos (`uint8` vs `float32`) sin utilizar funciones de “caja negra” para la matemática. Puede utilizar el esqueleto de código `lab_semana1.py` que se adjuntó en el portal. Se permite el uso de `numpy`, `opencv-python` (solo para I/O y conversiones de espacio de color) y `matplotlib`.

### Ejercicio 1: Contraste y Brillo Vectorizado

Implemente la función `manual_contrast_brightness(image, alpha, beta)`. Para ello, debe convertir la imagen a `float32`, normalizar, aplicar la fórmula lineal
$g(x) = \alpha f(x) + \beta$,
hacer *clipping* para asegurar el rango $[0, 1]$ y regresar a `uint8`.

Note que no puede usar `cv2.convertScaleAbs`. Debe hacerlo con pura manipulación de matrices NumPy.

### Ejercicio 2: Corrección Gamma Manual

Implemente la función `manual_gamma_correction(image, gamma)`. Para ello:

- Implemente la ecuación
  $V_{\text{out}} = V_{\text{in}}^{\gamma}$

- Recuerde que la operación de potencia es costosa. Aunque en producción usaríamos una LUT (*Look-Up Table*), aquí se requiere vectorizar la operación de potencia sobre la matriz flotante.

### Ejercicio 3: Segmentación Cromática

Implemente la función `hsv_segmentation(image)`. Para ello:

- Cargue una imagen de prueba (algo colorido).
- Conviértala a HSV.
- Defina manualmente los rangos `(lower_bound, upper_bound)` para aislar un color específico (ej. el amarillo de un banano o el rojo de una manzana).
- Genere una máscara binaria y úsela para mostrar solo el objeto segmentado sobre un fondo negro.

# Laboratorio 1

## Task 2 – Práctica

Se permite el uso de OpenCV únicamente para lectura y/o escritura de imágenes y visualización de las mismas, no para algoritmos de procesamiento. Es decir, está prohibido usar `cv2.filter2D`, `cv2.GaussianBlur`, `cv2.Sobel`, o `cv2.Canny`. Debe usar NumPy y operaciones matriciales.

> **Nota:** La dirección del gradiente $\theta$ se calcula y se retorna en **radianes**, utilizando la función $\arctan2(G_y, G_x)$.

### Ejercicio 1: Convolución 2D Genérica

Escriba una función `mi_convolucion(imagen, kernel, padding_type='reflect')`, considerando lo siguiente:

- **Restricción 1:** La función debe manejar imágenes en escala de grises.
- **Restricción 2:** Debe implementar el padding manualmente antes de operar.
- **Reto de optimización:** Intente no usar 4 bucles for anidados. Investigue cómo usar slicing de NumPy o `np.einsum` para hacerlo vectorizado, o al menos reduzca a 2 bucles.
- **Nota:** Recuerde que matemáticamente la convolución invierte el kernel. Implemente el *flip* del kernel dentro de la función.

#### Qué se hizo

Se implementó la convolución 2D como operación base, tomando la idea central de clase: un **kernel** (matriz pequeña) se "barre" sobre la imagen (matriz grande) y en cada posición se calcula un **producto punto** entre vecindad y kernel para producir un nuevo píxel. Esto corresponde a la "multiplicación programada" descrita en la intuición de convolución: se aplica un "programa" (kernel) localmente para obtener una salida más útil que el valor de un solo píxel.  

**Referencia:** [BetterExplained (intuición + por qué hay flip)](https://betterexplained.com/articles/intuitive-convolution/).

#### Convolución vs correlación (flip obligatorio)

Se aplicó el *flip* del kernel internamente para cumplir la definición de convolución (a diferencia de correlación). Se asumió que algunos kernels pueden ser simétricos (p.ej. gaussiano), pero se mantuvo el flip para ser correctos en general.  

**Referencia:** [BetterExplained](https://betterexplained.com/articles/intuitive-convolution/).

#### Manejo estricto de escala de grises

Se trabajó estrictamente con imágenes 2D ($H \times W$). Si una imagen venía en BGR, se convirtió a gris antes de cualquier operación, manteniendo el contrato "grayscale".

#### Padding manual

Se implementó padding manual porque en los bordes el kernel "se sale". Se priorizó `reflect` como opción por defecto, porque minimiza discontinuidades y evita introducir bordes artificiales (como con ceros), alineado con lo discutido en clase.  
La necesidad de padding también aparece al explicar cómo se mantiene tamaño y cómo afectan bordes.  

**Referencia:** [Medium (CNN convolution)](https://medium.com/analytics-vidhya/convolution-operations-in-cnn-deep-learning-compter-vision-128906ece7d3) para la motivación de padding y borde/tamaño.  

#### Optimización (sin 4 bucles)

Se evitó el enfoque de 4 bucles anidados. La estrategia fue reducir la operación a *crear una vista por ventanas (vecindades) con slicing/estriding, y hacer la suma de productos con una operación vectorizada*.

Para el cómputo vectorizado se contempló `np.einsum` como herramienta directa para expresar la suma de productos entre ventanas y kernel.s

**Referencia:** Documentación de [`einsum`](https://numpy.org/doc/stable/reference/generated/numpy.einsum.html).  

### Ejercicio 2: Generador de Gaussianos

Escriba una función `generar_gaussiano(tamano, sigma)`. Para ello considere:

- La función debe devolver una matriz cuadrada de tamaño $tamano \times tamano$ con los coeficientes de una distribución Gaussiana 2D centrada.
- **Importante:** Asegúrese de que la suma de todos los elementos de la matriz sea igual a $1.0$ (Normalización).

#### Qué se hizo

Se generó un kernel gaussiano 2D centrado, porque en clase se justificó que el **Box Filter** introduce desenfoque "duro" y puede degradar la localización de estructuras, mientras que el Gaussiano realiza un suavizado más natural: asigna más peso al centro y decae con la distancia, preservando mejor bordes relevantes.

Se construyó una grilla centrada (coordenadas alrededor de 0) y se evaluó la Gaussiana 2D con pesos decrecientes según la distancia al centro.

#### Normalización (suma = 1.0)

Se normalizó el kernel para asegurar que la suma total fuese exactamente $1.0$. Esto mantiene el nivel promedio de intensidad y evita cambios globales de brillo al filtrar.

Referencia (concepto y motivación de blur gaussiano y rol de $\sigma$):  

- https://himani-gulati.medium.com/understanding-the-gaussian-filter-c2cb4fb4f16b  

- https://www.educative.io/answers/what-is-gaussian-blur-in-image-processing

#### Rol de $\sigma$

Se trató $\sigma$ como el control del nivel de suavizado: valores mayores suavizan más (reducen detalle fino) y valores menores suavizan menos, coherente con el preprocesamiento típico antes de derivadas/gradientes para reducir falsos bordes por ruido.

### Ejercicio 3: Pipeline de Detección de Bordes (Sobel)

Cree una función `detectar_bordes_sobel(imagen)`. Para ello considere:

- Aplique los kernels de Sobel $G_x$ y $G_y$ usando su función `mi_convolucion`.
- Calcule y retorne dos matrices:
  - **Magnitud del gradiente:**  
    $$
    G = \sqrt{G_x^2 + G_y^2}
    $$
    (Normalizada a 0–255 para visualizar)
  - **Dirección del gradiente:**  
    $$
    \theta = \arctan2(G_y, G_x)
    $$
    (En radianes o grados)

#### Qué se hizo

Se implementó el pipeline de Sobel como se discutió en clase: un borde se modela como un **cambio de intensidad** (derivada). Como las imágenes son discretas, se aproximó la derivada mediante **diferencias finitas** usando kernels Sobel.

Se definieron los kernels $G_x$ y $G_y$ y se aplicaron usando **nuestra propia** `mi_convolucion`, cumpliendo la restricción de no usar Sobel de OpenCV.

#### Magnitud del gradiente

Se calculó la magnitud:
$$
G = \sqrt{G_x^2 + G_y^2}
$$
y se normalizó a 0–255 para visualización. Esto coincide con el objetivo de producir un mapa de bordes interpretable.

#### Dirección del gradiente

Se calculó la dirección:
$$
\theta = \arctan2(G_y, G_x)
$$

usando `np.arctan2`, que elige el cuadrante correctamente (ángulo en $[-\pi, \pi]$).  

**Referencia:** documentación oficial de [`arctan2`](https://numpy.org/doc/stable/reference/generated/numpy.arctan2.html).  

### Resultados

Al aplicar Sobel directamente sobre la imagen original (**raw**), la magnitud del gradiente muestra una gran cantidad de bordes finos. Esto ocurre porque Sobel responde a **cualquier variación local de intensidad**, incluyendo textura y ruido. Como resultado, el mapa de bordes es más cargado y menos selectivo.

Al introducir un **suavizado Gaussiano previo** ($\sigma = 1$, kernel 5×5), el comportamiento cambia de forma clara. La imagen suavizada elimina variaciones pequeñas, y el Sobel aplicado posteriormente produce un mapa de bordes **más limpio y legible**, donde se resaltan principalmente las estructuras importantes.

En la **dirección del gradiente**, el caso *raw* presenta orientaciones muy variables y poco estables debido al ruido. En cambio, con suavizado, la dirección $\theta$ se vuelve **más coherente**, disminuye la cantidad de direcciones irrelevantes y los bordes aparecen mejor definidos y continuos.

> Esto confirma que aplicar un Gaussiano antes de Sobel mejora la calidad del gradiente y prepara mejor la imagen para etapas posteriores de detección de bordes.

![Test Imagen 1](../images/task2.result-image1.png)

![Test Imagen 2](../images/task2.result-image2.png)

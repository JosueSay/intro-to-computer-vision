# Laboratorio 1

## Task 2 – Práctica

Se permite el uso de OpenCV únicamente para lectura y/o escritura de imágenes y visualización de las mismas, no para algoritmos de procesamiento. Es decir, está prohibido usar `cv2.filter2D`, `cv2.GaussianBlur`, `cv2.Sobel`, o `cv2.Canny`. Debe usar NumPy y operaciones matriciales.

### Ejercicio 1: Convolución 2D Genérica

Escriba una función `mi_convolucion(imagen, kernel, padding_type='reflect')`, considerando lo siguiente:

- **Restricción 1:** La función debe manejar imágenes en escala de grises.
- **Restricción 2:** Debe implementar el padding manualmente antes de operar.
- **Reto de optimización:** Intente no usar 4 bucles for anidados. Investigue cómo usar slicing de NumPy o `np.einsum` para hacerlo vectorizado, o al menos reduzca a 2 bucles.
- **Nota:** Recuerde que matemáticamente la convolución invierte el kernel. Implemente el *flip* del kernel dentro de la función.

### Ejercicio 2: Generador de Gaussianos

Escriba una función `generar_gaussiano(tamano, sigma)`. Para ello considere:

- La función debe devolver una matriz cuadrada de tamaño $tamano \times tamano$ con los coeficientes de una distribución Gaussiana 2D centrada.
- **Importante:** Asegúrese de que la suma de todos los elementos de la matriz sea igual a $1.0$ (Normalización).

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

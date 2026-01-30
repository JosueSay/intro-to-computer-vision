# Laboratorio 1

## Task 2

Está desarrollando un sistema biométrico de seguridad. El sensor de huellas dactilares está sucio y produce imágenes binarias con dos tipos de defectos:

1. Pequeños puntos blancos en los valles negros de la huella (ruido sal).
2. Las crestas de la huella presentan pequeñas roturas que impiden el matching (grietas).

### Estrategia

Se utilizó una secuencia de operaciones morfológicas sobre una imagen binaria, con el objetivo de:

1. Eliminar el ruido blanco aislado sin afectar las crestas.
2. Conectar las roturas presentes en las crestas de la huella.

La solución se basa en el uso controlado de **apertura** y **cierre**, aplicadas de forma secuencial.

### Inciso 1. Binarización

La imagen `fingerprint_noisy.png` se cargó en escala de grises y se binarizó utilizando umbralización de Otsu, asegurando una imagen binaria limpia con valores `{0, 255}`.

Posteriormente, se verificó que las crestas de la huella correspondieran al foreground (blanco). En caso contrario, la imagen fue invertida para garantizar que las operaciones morfológicas actuaran correctamente sobre las crestas.

### Inciso 2. Eliminación de ruido sal

- **Operación aplicada:** Apertura morfológica (erosión → dilatación).
- **Elemento estructurante:** Elipse.
- **Tamaño:** 3×3.

**Justificación:**  

El ruido presente corresponde a píxeles blancos pequeños y aislados.  
La apertura elimina estos puntos durante la erosión, y la dilatación posterior restaura el grosor de las crestas sin reintroducir el ruido.  
Esta operación permite limpiar la imagen sin destruir la estructura principal de la huella.

### Inciso 3. Conexión de grietas

- **Operación aplicada:** Cierre morfológico (dilatación → erosión).
- **Elemento estructurante:** Elipse.
- **Tamaño:** 5×5.

**Justificación:**

Las crestas presentan pequeñas discontinuidades.  
La dilatación conecta segmentos cercanos cuya separación es menor que el elemento estructurante, y la erosión posterior corrige el engrosamiento producido, preservando la forma general de las crestas.

### Inciso 4. Resultados

Se muestran tres imágenes:

1. Imagen original binaria.
2. Imagen tras aplicar apertura (eliminación de ruido sal).
3. Imagen final tras aplicar cierre (crestas continuas).

La imagen final presenta **menor ruido y mayor continuidad**, cumpliendo con los requisitos del preprocesamiento para sistemas biométricos.

### ¿El orden de los factores altera el producto?

Sí. Las operaciones morfológicas no son conmutativas, por lo que el orden altera el resultado en términos teóricos.

#### Orden aplicado

- **Apertura → Cierre**

Este orden elimina primero el ruido blanco aislado y luego conecta las grietas reales de las crestas.

#### Orden inverso evaluado

- **Cierre → Apertura**

En este caso particular, ambos resultados son **visualmente similares**, sin embargo se observa que en el pipeline **Cierre → Apertura** los **detalles finos de las crestas se mantienen ligeramente más notorios** en comparación con **Apertura → Cierre**.

Esto ocurre porque el cierre inicial refuerza las crestas mediante dilatación antes de aplicar la apertura, mientras que en el orden original la apertura elimina primero información fina junto con el ruido.

Aun así:

- El ruido sal es pequeño.
- Las grietas son cortas.

Por lo tanto, ambos órdenes convergen a resultados cercanos, confirmando que la diferencia es **sutil pero observable**.

La demostración visual confirma que se evaluaron ambos órdenes y refuerza que, aunque en este ejemplo los resultados sean parecidos, **apertura y cierre no son conmutativas**.

![Apertura Cierre](../images/task2.result1.png)
  
![Cierre Apertura](../images/task2.result2.png)

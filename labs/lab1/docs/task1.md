# Laboratorio 1

## Task 1 - Análisis Teórico

Considerando el escenario previamente planteado, conteste:

### Pregunta 1

Su jefe sugiere usar un filtro de media (Box Filter) de 7x7 para eliminar el ruido rápido. Usted cree que es una mala idea. Explique matemáticamente y con un diagrama visual (dibujado) por qué un Box Filter de ese tamaño es perjudicial para la detección precisa de la posición de un obstáculo comparado con un filtro Gaussiano del mismo tamaño.

**Idea:** Un Box Filter 7×7 promedia todos los píxeles por igual, lo que termina desplazando y degradando la ubicación real de un borde. El filtro Gaussiano 7×7 también suaviza el ruido, pero asigna mayor peso a los píxeles cercanos al centro, conservando mejor la posición del obstáculo.

**Box Filter (media) 7×7:**

- Cada elemento del kernel tiene el mismo peso:
  
  peso = 1 / 49

- El valor de salida de un píxel se calcula como el promedio de todos los valores dentro de la ventana 7×7:

  I_salida(x, y) = (1/49) * suma de I(x+u, y+v)  
  donde u y v van de -3 a 3

- Problema para detección de obstáculos:
  - El borde se mezcla con píxeles de ambos lados con el mismo peso.
  - El contraste del borde disminuye (el borde se ve más “gris”).
  - La transición se ensancha.
  - La posición exacta del borde puede desplazarse porque influyen muchos píxeles lejanos.

**Filtro Gaussiano 7×7:**

- El peso de cada píxel depende de su distancia al centro:

  h(i,j) = (1 / (2 *pi* sigma²)) *exp( - (i² + j²) / (2* sigma²) )

- Luego el kernel se normaliza para que la suma total sea 1.

- Diferencia clave:
  - Los píxeles centrales pesan más.
  - Los píxeles lejanos pesan menos.
  - Se reduce el ruido sin destruir tanto la pendiente del borde.

**Por qué el Box 7×7 es peor para localizar obstáculos:**

En detección de bordes (Sobel, Laplaciano, Canny) se buscan cambios locales fuertes.  
Un Box Filter grande promedia demasiado, haciendo que:

- Los bordes sean más débiles.
- Algunos bordes no superen el umbral.
- La textura del suelo se mezcle con obstáculos, causando detecciones imprecisas.

**Diagrama visual (dibujado a mano):**

Se puede dibujar una señal 1D tipo escalón:

- Original: cambio brusco.
- Box 7×7: rampa ancha y desplazada.
- Gaussiano 7×7: rampa más suave pero centrada.

## Pregunta 2

Al realizar la convolución en los bordes de la imagen (por ejemplo, en el píxel (0,0), el kernel "se sale" de la imagen).

   a. Si el robot navega por pasillos oscuros con luces brillantes al final, ¿por qué el Zero-Padding podría generar falsos positivos de bordes en la periferia de la imagen?

   b. ¿Qué estrategia de padding (Reflect, Replicate, Wrap) recomendaría para evitar esto y por qué?

Al realizar la convolución en los bordes de la imagen (por ejemplo en el píxel (0,0)), parte del kernel queda fuera de la imagen.

### a. ¿Por qué Zero-Padding genera falsos positivos?

Con Zero-Padding, los píxeles fuera de la imagen se asumen con valor 0.  
En un pasillo oscuro con zonas brillantes, esto crea un contraste artificial entre:

- píxeles reales  
- píxeles con valor 0

Al aplicar operadores de borde, este salto artificial genera gradientes fuertes que **no existen realmente**, produciendo falsos bordes en la periferia de la imagen.

### b. Estrategia de padding recomendada

Se recomienda **Reflect Padding**.

**Razones:**

- Refleja los valores reales de la imagen.
- Mantiene continuidad de intensidades.
- Evita saltos bruscos artificiales.
- Reduce detecciones falsas cerca de los bordes.

Comparación rápida:

- Replicate: repite el borde (aceptable).
- Wrap: mezcla lados opuestos (no realista).
- Reflect: más estable para visión robótica.

## Pregunta 3

Dada la siguiente sub-imagen I de 3x3 y el kernel K:

   a. Calcule el valor del píxel central resultante de la convolución

   Se multiplican los valores correspondientes y se suman:

   0·10 + 1·10 + 0·10  

- 1·10 + (-4)·0 + 1·10  
- 0·10 + 1·10 + 0·10  

   = 10 + 10 + 10 + 10  
   = **40**

   **Resultado:** 40

   > Nota: El kernel es simétrico, por lo que el flip de la convolución no cambia el resultado.

   b. ¿Qué tipo de estructura detecta este filtro K (conocido como Laplaciano)?

   Este kernel es un **Laplaciano 4-conexo**, un operador de segunda derivada.

   Detecta:

- Bordes
- Esquinas
- Cambios bruscos de intensidad
- Puntos aislados

   En este caso, el centro es muy distinto a sus vecinos, por lo que el filtro responde con un valor alto, indicando una discontinuidad fuerte.

![Task 3 - Inciso 3](../images/tast1.question3.png)

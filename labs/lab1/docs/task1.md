# Laboratorio 1

## Task 1 - Análisis Teórico

Considerando el escenario previamente planteado, conteste:

### Pregunta 1

Su jefe sugiere usar un filtro de media (Box Filter) de 7x7 para eliminar el ruido rápido. Usted cree que es una mala idea. Explique matemáticamente y con un diagrama visual (dibujado) por qué un Box Filter de ese tamaño es perjudicial para la detección precisa de la posición de un obstáculo comparado con un filtro Gaussiano del mismo tamaño.

## Pregunta 2

Al realizar la convolución en los bordes de la imagen (por ejemplo, en el píxel (0,0), el kernel "se sale" de la imagen).

   a. Si el robot navega por pasillos oscuros con luces brillantes al final, ¿por qué el Zero-Padding podría generar falsos positivos de bordes en la periferia de la imagen?

   b. ¿Qué estrategia de padding (Reflect, Replicate, Wrap) recomendaría para evitar esto y por qué?

## Pregunta 3

Dada la siguiente sub-imagen I de 3x3 y el kernel K:

   a. Calcule el valor del píxel central resultante de la convolución

   b. ¿Qué tipo de estructura detecta este filtro K (conocido como Laplaciano)?

![Task 3 - Inciso 3](../images/tast1.question3.png)

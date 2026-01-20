# Hoja de Trabajo 1

## Task 3 – Preguntas Post-Práctica

Responda brevemente (máximo 3 líneas por respuesta):

1. En la diapositiva 15 se mencionó que *“Iterar píxel a píxel en Python es un Pecado Capital”*. Explique, en términos de gestión de memoria y CPU, por qué una operación vectorizada en NumPy es órdenes de magnitud más rápida que un *for loop*.

- R: NumPy ejecuta operaciones en C sobre bloques contiguos de memoria, procesando miles de píxeles simultáneamente en lugar de uno por uno. Y esto ayuda a evitar el overhead del intérprete de Python en cada iteración y aprovecha mejor el caché del CPU, siendo miles de veces más rápido que un for loop normal

2. Al visualizar imágenes con `matplotlib`, ¿qué sucede si olvida que OpenCV carga las imágenes en formato BGR? ¿Cómo se ve visualmente el error?

- R: Pues los formatos indican el orden de los canales de color, para RGB es rojo, verde, azul y para BGR es azul, verde, rojo. Por lo que al cargar la imágen con formato BGR vamos a ver que los canales rojo y azul estan intercambiados.

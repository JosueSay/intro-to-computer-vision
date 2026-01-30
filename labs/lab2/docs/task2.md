# Laboratorio 1

## Task 2 – Práctica

Está desarrollando un sistema biométrico de seguridad. El sensor de huellas dactilares está sucio y produce imágenes binarias con dos tipos de defectos:

1. Pequeños puntos blancos en los valles negros de la huella (Ruido Sal)
2. Las “crestas” de la huella tienen pequeñas roturas que impiden que el algoritmo de matching funcione (grietas).

Para esta parte se espera que su entregable muestre:

- Selección correcta de los Elementos Estructurantes (Forma y Tamaño) para cada paso.
- Calidad visual de la imagen final (sin ruido y continua)
- Responda: ¿El orden de los factores altera el producto? Explique qué hubiera pasado si hubiera aplicado las operaciones en orden inverso y demuéstrelo con un ejemplo visual en el notebook.

### Inciso 1

Cargue la imagen fingerprint_noisy.png. Asegúrese de que sea binaria.

### Inciso 2

Aplique una operación morfológica para eliminar el ruido blanco sin destruir las crestas de la huella. (Seleccione entre Erosión, Dilatación, Apertura o Cierre).

### Inciso 3

Aplique una segunda operación secuencial para conectar las grietas en las crestas de la huella.

### Inciso 4

Muestre la imagen original, la imagen tras el paso 2, y la imagen final.

# Laboratorio 1

## Task 2 – Práctica

Está desarrollando un sistema biométrico de seguridad. El sensor de huellas dactilares está sucio y produce imágenes binarias con dos tipos de defectos:

1. Pequeños puntos blancos en los valles negros de la huella (Ruido Sal)
2. Las “crestas” de la huella tienen pequeñas roturas que impiden que el algoritmo de matching funcione (grietas).

### Estrategia

**Idea general:** usar una **secuencia de operaciones morfológicas** con elementos estructurantes (SE) pequeños para:

1. **eliminar “sal”** (puntos blancos aislados) sin dañar crestas, y luego
2. **cerrar grietas** (pequeñas rupturas) para recuperar continuidad.

**1. Preparación (Inciso 1: binaria real)**

- Cargar `fingerprint_noisy.png` en escala de grises.

- Binarizar y verificar que solo existan valores {0, 255}.

- Confirmar qué representa el **foreground** (1/255): idealmente que las **crestas** queden como blanco. Si quedaran al revés, se invierte (esto importa porque erosión/dilatación actúan sobre el foreground).

**2.Eliminar ruido sal (Inciso 2)**

- Operación elegida: **Apertura (Erosión → Dilatación)**.

  - Justificación: la apertura se usa para **remover “salt noise” (puntos blancos)** y es menos destructiva que aplicar erosión sola, porque recupera forma tras la dilatación. (Del artículo de Opening: “Removing Salt Noise… opening (erosion followed by dilation)” y definición de opening).
- **SE recomendado:** pequeño y “isotrópico” (cuadrado o disco).

  - Tamaño inicial típico: **3×3**; si el ruido es más grande, probar **5×5**.
  - Criterio: el SE debe ser **ligeramente mayor** que los puntos de ruido para que desaparezcan en la erosión, pero **no tan grande** como para romper/adelgazar demasiado las crestas.

**Entregable que se documenta aquí:** explicar por qué apertura y por qué ese SE (forma/tamaño) en términos de “mata puntos aislados y preserva estructuras grandes”.

**3. Conectar grietas en crestas (Inciso 3)**

- Operación elegida: **Cierre (Dilatación → Erosión)**.

  - Justificación: la dilatación **conecta regiones separadas** si la separación es menor que el SE; luego la erosión “reajusta” el grosor. (GeeksforGeeks: dilatación “fills holes and broken areas” y “connects areas separated by space smaller than structuring element”; además, el cierre usa dilatación primero).
- **SE recomendado:**

  - Si las grietas son pequeñas y en varias direcciones: **disco/cuadrado 3×3 o 5×5**.
  - Si las grietas parecen orientadas (p.ej., cortes más horizontales): **SE lineal** (una línea corta) alineada con la dirección donde quieres “puentear” la rotura.
- Criterio: elegir el tamaño mínimo que **cierra las grietas** sin pegar crestas que no deberían unirse.

**4. Visualización (Inciso 4)**
Mostrar en el notebook, en el mismo tamaño y con títulos:

1. Imagen original binaria
2. Resultado tras **Apertura** (paso 2)
3. Resultado final tras **Cierre** (paso 3)

**5. ¿El orden altera el producto?**

**Demostración:**

---

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

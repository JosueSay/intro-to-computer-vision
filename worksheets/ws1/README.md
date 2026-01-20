# Hoja de Trabajo 1 - Visión por Computadora
**Task 1: Análisis Teórico**

---

## 1. Dimensionamiento de Hardware (Conducción Autónoma)

**Datos Generales:**
* **Cámaras:** 8
* **Resolución:** 4K UHD ($3840 \times 2160$)
* **Profundidad:** 12 bits (Raw Bayer)
* **Framerate:** 60 FPS

### a. Tamaño exacto de un frame crudo (MB)

Primero calculamos la cantidad total de bits por imagen y luego realizamos las conversiones a Bytes y Megabytes (usando la base binaria $1024^2$, estándar en sistemas operativos).

$$\text{Píxeles totales} = 3840 \times 2160 = 8,294,400 \text{ px}$$
$$\text{Bits totales} = 8,294,400 \times 12 \text{ bits} = 99,532,800 \text{ bits}$$

Convertimos a Bytes ($1 \text{ B} = 8 \text{ bits}$):
$$\text{Tamaño en Bytes} = \frac{99,532,800}{8} = 12,441,600 \text{ Bytes}$$

Convertimos a Megabytes ($1 \text{ MB} = 1024 \times 1024 \text{ B}$):
$$\text{Tamaño en MB} = \frac{12,441,600}{1,048,576} \approx \mathbf{11.86 \text{ MB}}$$

### b. Ancho de banda necesario (Gbps)

Calculamos el flujo de datos total por segundo para las 8 cámaras sin compresión.

$$\text{Bits por segundo} = (\text{bits por frame}) \times (\text{cámaras}) \times (\text{FPS})$$
$$\text{bps} = 99,532,800 \times 8 \times 60 = 47,775,744,000 \text{ bits/s}$$

Convertimos a Gigabits por segundo (usando base decimal $10^9$ para telecomunicaciones):
$$\text{Bandwidth} = \frac{47,775,744,000}{10^9} \approx \mathbf{47.78 \text{ Gbps}}$$

### c. Capacidad del buffer de video (16 GB RAM)

Para determinar los segundos de historia, primero necesitamos la tasa de llenado de la memoria (Throughput) en las mismas unidades que la RAM (Gigabytes binarios o GiB).

* Tasa de entrada: $12,441,600 \text{ Bytes/frame} \times 8 \times 60 = 5,971,968,000 \text{ Bytes/s}$
* Tasa en GB: $5,971,968,000 / 1024^3 \approx 5.56 \text{ GB/s}$

$$\text{Tiempo} = \frac{\text{Memoria Total}}{\text{Tasa de Entrada}} = \frac{16 \text{ GB}}{5.56 \text{ GB/s}} \approx \mathbf{2.87 \text{ segundos}}$$

### d. Viabilidad de transmisión 5G a la nube

**Respuesta: No es viable.**

**Justificación:**
El cálculo del inciso (b) arroja un requerimiento de **~47.8 Gbps** de subida (uplink). Aunque el marketing de 5G promete velocidades pico teóricas altas (10-20 Gbps en descarga), la velocidad de **subida** real en condiciones óptimas rara vez supera 1 Gbps (incluso con mmWave). El ancho de banda requerido excede la capacidad actual de la infraestructura por un factor de casi 50x. Es arquitectónicamente obligatorio procesar en el borde (Edge Computing) o aplicar compresión agresiva antes de transmitir.

---

## 2. Procesamiento de Imagen (Pipeline Secuencial)

**Datos:**
* Input ($I_{in}$): 50 (uint8)
* Gamma ($\gamma$): 0.5
* Lineal ($\alpha$): 1.2
* Brillo ($\beta$): -10 (escala 0-255)

### a. Valor final del píxel $I_{out}$ (flotantes normalizados)

1.  **Normalización [0, 1]:**
    $$I_{norm} = \frac{50}{255} \approx 0.196078$$

2.  **Corrección Gamma ($Y=0.5$):**
    $$V_{gamma} = (I_{norm})^{0.5} = \sqrt{0.196078} \approx 0.442807$$

3.  **Ajuste Lineal:**
    Primero normalizamos $\beta$ al dominio flotante: $\beta_{norm} = -10/255 \approx -0.039216$.
    $$I_{lin} = (\alpha \times V_{gamma}) + \beta_{norm}$$
    $$I_{lin} = (1.2 \times 0.442807) - 0.039216$$
    $$I_{lin} = 0.531368 - 0.039216 = 0.492152$$

4.  **Conversión a uint8:**
    $$I_{out} = I_{lin} \times 255 = 0.492152 \times 255 \approx 125.49$$
    
    Redondeando: **$I_{out} = 125$**

### b. ¿Hubo saturación (clipping)?

**No.** El valor resultante en el dominio flotante ($0.492$) se mantuvo estrictamente dentro del rango $[0, 1]$, por lo que no fue necesario recortar valores que excedieran los límites.

### c. Error numérico por truncamiento (uso directo de uint8)

Si simulamos el proceso con enteros (truncando decimales):

1.  **Gamma (aprox en enteros):** $255 \times (50/255)^{0.5} = 112.9 \rightarrow \text{trunc}(112)$.
2.  **Lineal:** $(1.2 \times 112) - 10 = 134.4 - 10 = 124.4 \rightarrow \text{trunc}(124)$.

* Resultado Flotante: **125.5**
* Resultado Entero: **124**

**Error:** Existe una desviación de aproximadamente **1.5 niveles de intensidad**. En procesamiento de video o gradientes suaves, este error acumulado causaría *banding* visible.

---

## 3. Espacios de Color (Robot Clasificador)

**Objetos:**
* Pelota Sol (Rojo): $R_{rgb} = (255, 0, 0)$
* Pelota Sombra (Rojo oscuro): $S_{rgb} = (50, 0, 0)$

### a. Distancia Euclidiana en RGB

$$d = \sqrt{(R_1-R_2)^2 + (G_1-G_2)^2 + (B_1-B_2)^2}$$
$$d = \sqrt{(255-50)^2 + 0 + 0} = \sqrt{205^2} = \mathbf{205}$$

*(Una distancia inmensa considerando que el máximo posible es $\approx 441$).*

### b. Conversión a HSV (Normalizado)

**Para $R_{rgb} (255, 0, 0)$:**
* $R'=1, G'=0, B'=0$. Max=1, Min=0.
* Hue ($H$): 0 (Rojo puro).
* Sat ($S$): $(1-0)/1 = 1$.
* Val ($V$): 1.
* **$HSV_{sol} = (0, 1, 1)$**

**Para $S_{rgb} (50, 0, 0)$:**
* $R'=50/255 \approx 0.196$. Max=0.196, Min=0.
* Hue ($H$): 0.
* Sat ($S$): $(0.196-0)/0.196 = 1$.
* Val ($V$): 0.196.
* **$HSV_{sombra} = (0, 1, 0.196)$**

### c. Diferencia absoluta canal por canal

* $\Delta H = |0 - 0| = \mathbf{0}$
* $\Delta S = |1 - 1| = \mathbf{0}$
* $\Delta V = |1 - 0.196| = \mathbf{0.804}$

### d. Argumentación matemática (Clustering RGB vs HSV)

Un algoritmo de clustering simple (como K-Means o umbralización esférica) en **RGB** fallaría porque la distancia euclidiana entre los vectores es de **205**. El algoritmo interpretaría esto como dos objetos de clases totalmente distintas (ej. "Rojo brillante" vs "Negro/Gris"), ya que la magnitud de la intensidad domina el cálculo de la distancia.

En cambio, en **HSV**, los canales que definen la "cromaticidad" del objeto ($H$ y $S$) tienen una distancia de **0**. La única variación ocurre en $V$ (brillo). Al usar HSV, podemos configurar el algoritmo para que agrupe basándose estrictamente en $H$ y $S$, ignorando la varianza en $V$. Esto hace al sistema **invariante a la iluminación**, permitiendo identificar correctamente que ambos píxeles pertenecen a la misma "pelota roja".
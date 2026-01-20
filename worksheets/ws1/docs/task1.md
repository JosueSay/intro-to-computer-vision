# Hoja de Trabajo 1

## Task 1 - Análisis Teórico

Considere cada uno de los siguientes escenarios y responda según corresponda.

## Pregunta 1

Como director de un proyecto de conducción autónoma, debe dimensionar el hardware para un nuevo vehículo. El sistema utiliza 8 cámaras que capturan video a resolución 4K UHD $(3840 \times 2160)$. Debido a la necesidad de alto rango dinámico (HDR), los sensores operan a 12 bits por píxel (Raw Bayer Pattern) a 60 FPS. Métrica A: enfocada puramente en el flujo vehicular.

1. Calcule el tamaño exacto de una sola imagen (frame) cruda en megabytes (MB).

2. Calcule el ancho de banda necesario (en Gbps) para transmitir el flujo de las 8 cámaras al procesador central sin compresión.

3. Si su procesador tiene una memoria RAM reservada de 16 GB exclusivamente para el buffer de video, ¿cuántos segundos de historia puede almacenar antes de empezar a sobrescribir datos?

4. Basado en su resultado, ¿es viable enviar estos datos “crudos” a la nube en tiempo real usando 5G? Justifique.

## Pregunta 2

Considere un píxel con valor de intensidad $I_{in} = 50$ en una imagen estándar de 8 bits $(0{-}255)$. Se aplican dos procesos de mejora secuenciales en el siguiente orden:

1. Corrección gamma con $\gamma = 0.5$ (para expandir sombras).
2. Ajuste lineal con ganancia $\alpha = 1.2$ y brillo $\beta = -10$ (para contrastar).

Realice los cálculos en el dominio de flotantes normalizados $[0,1]$, como dicta la buena práctica, y convierta a entero de 8 bits solo al final.

1. Calcule el valor final del píxel $I_{out}$.
2. ¿Hubo saturación (clipping) en el proceso?
3. Si hubiéramos realizado las operaciones usando `uint8` directamente sin convertir a `float` (truncando decimales en cada paso intermedio), ¿cuál habría sido el error numérico resultante?

## Pregunta 3

Usted está programando un robot clasificador de pelotas. Tiene dos objetos: una pelota roja brillante bajo el sol $R_{rgb} = (255, 0, 0)$ y la misma pelota roja en una sombra profunda $S_{rgb} = (50, 0, 0)$.

1. Calcule la distancia entre estos dos colores en el espacio RGB.
2. Convierta ambos colores al espacio HSV (asuma rangos normalizados $H \in [0,1]$, $S \in [0,1]$, $V \in [0,1]$ para simplificar, sabiendo que el Hue del rojo es $0$).
3. Calcule la diferencia absoluta canal por canal en HSV.
4. Argumente matemáticamente por qué un algoritmo de agrupación (clustering) simple fallaría en RGB pero funcionaría en HSV para determinar que ambos píxeles pertenecen al mismo objeto “pelota roja”.

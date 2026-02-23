import cv2
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from tabulate import tabulate


def measureDisparityWithClicks(image, objectName):
    """
    Selecciona 2 puntos, retorna Devuelve |x1 - x2|:
    - Primero: fantasma rojo
    - Segundo: fantasma cian
    """
    plt.figure(figsize=(8,6))
    plt.imshow(image)
    plt.title(f"Seleccione 2 puntos para {objectName} (Rojo luego Cian)")
    plt.axis("on")

    points = plt.ginput(2)
    plt.close()

    if len(points) != 2:
        raise ValueError("Debe seleccionar exactamente 2 puntos.")

    (x1, y1), (x2, y2) = points

    disparity = abs(x1 - x2)

    print(f"\n{objectName}")
    print(f"\tCoordenada 1: ({x1:.2f}, {y1:.2f})")
    print(f"\tCoordenada 2: ({x2:.2f}, {y2:.2f})")
    print(f"\tDisparidad en píxeles: {disparity:.2f}")

    return x1, x2, disparity


# Cargar imagen anaglifo
anaglyph_path = "./images/results/task2.1.png"
img_bgr = cv2.imread(anaglyph_path)

if img_bgr is None:
    raise FileNotFoundError(f"No se encontró la imagen {anaglyph_path}")

anaglyph = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


# Medir objetos
x1_A, x2_A, dispA = measureDisparityWithClicks(anaglyph, "Objeto A (Cercano)")
x1_B, x2_B, dispB = measureDisparityWithClicks(anaglyph, "Objeto B (Medio)")
x1_C, x2_C, dispC = measureDisparityWithClicks(anaglyph, "Objeto C (Fondo)")

resultsTable = pd.DataFrame({
    "Objeto": ["A (Cercano)", "B (Medio)", "C (Fondo)"],
    "Distancia Real Estimada": ["~0.5 m", "~2 m", ">5 m"],
    "Coordenada X Fantasma 1": [x1_A, x1_B, x1_C],
    "Coordenada X Fantasma 2": [x2_A, x2_B, x2_C],
    "Disparidad (px)": [dispA, dispB, dispC]
})

print("\nResultados finales:")
print(tabulate(resultsTable, headers="keys", tablefmt="github", showindex=False))

log_path = "./images/results/task2.1.log"
csv_path = "./images/results/task2.1.csv"

with open(log_path, "w", encoding="utf-8") as f:
    f.write(tabulate(resultsTable, headers="keys", tablefmt="github", showindex=False))
    f.write("\n")

resultsTable.to_csv(csv_path, index=False)
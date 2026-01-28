import os
import glob
import shutil
import cv2
import numpy as np
import matplotlib.pyplot as plt
import kagglehub

from task2 import toGray, mi_convolucion, generar_gaussiano, detectar_bordes_sobel


def ensureDir(path):
    os.makedirs(path, exist_ok=True)


def getProjectRoot():
    return os.path.dirname(os.path.abspath(__file__))


def downloadDatasetToProject():
    # 1. Descarga y cachea el dataset desde Kaggle y copiarlo a sitio actual
    cachedPath = kagglehub.dataset_download("rajneesh231/salt-and-pepper-noise-images")
    root = getProjectRoot()
    localBase = os.path.join(root, "datasets")
    ensureDir(localBase)

    localPath = os.path.join(localBase, "salt-and-pepper-noise-images")

    if not os.path.exists(localPath):
        shutil.copytree(cachedPath, localPath, dirs_exist_ok=True)

    return localPath


def pickNoisyImage(datasetPath, index=0):
    noisyDir = os.path.join(datasetPath, "Noisy_folder")
    files = sorted(glob.glob(os.path.join(noisyDir, "*.*")))
    if len(files) == 0:
        raise RuntimeError(f"No se encontraron imágenes en: {noisyDir}")
    index = int(np.clip(index, 0, len(files) - 1))
    return files[index]


def sobelMagnitudeWithOptionalGaussian(gray, sigma=None, ksize=None):
    if sigma is None:
        G, _ = detectar_bordes_sobel(gray)
        return G

    k = generar_gaussiano(tamano=int(ksize), sigma=float(sigma))
    smooth = mi_convolucion(gray, k, padding_type="reflect")
    G, _ = detectar_bordes_sobel(smooth)
    return G


def experimentA(imagePath, outDir="images"):
    ensureDir(outDir)

    bgr = cv2.imread(imagePath, cv2.IMREAD_COLOR)
    gray = toGray(bgr)

    G_raw = sobelMagnitudeWithOptionalGaussian(gray, sigma=None, ksize=None)
    G_s1 = sobelMagnitudeWithOptionalGaussian(gray, sigma=1, ksize=5)
    G_s5 = sobelMagnitudeWithOptionalGaussian(gray, sigma=5, ksize=31)

    # base = os.path.splitext(os.path.basename(imagePath))[0]
    # out1 = os.path.join(outDir, f"task3.A.{base}.sobel.raw.png")
    # out2 = os.path.join(outDir, f"task3.A.{base}.sobel.sigma1.png")
    # out3 = os.path.join(outDir, f"task3.A.{base}.sobel.sigma5.png")

    # cv2.imwrite(out1, G_raw.astype(np.uint8))
    # cv2.imwrite(out2, G_s1.astype(np.uint8))
    # cv2.imwrite(out3, G_s5.astype(np.uint8))

    fig, axs = plt.subplots(1, 4, figsize=(18, 5), gridspec_kw={"wspace": 0.2})
    fig.canvas.manager.set_window_title("Task 3 - Experimento A (Sigma)")

    axs[0].imshow(gray, cmap="gray")
    axs[0].set_title("Noisy (gray)")
    axs[0].axis("off")

    axs[1].imshow(G_raw, cmap="gray")
    axs[1].set_title("Sobel |G| (sin suavizado)")
    axs[1].axis("off")

    axs[2].imshow(G_s1, cmap="gray")
    axs[2].set_title("Sobel |G| (Gauss sigma=1, 5x5)")
    axs[2].axis("off")

    axs[3].imshow(G_s5, cmap="gray")
    axs[3].set_title("Sobel |G| (Gauss sigma=5, 31x31)")
    axs[3].axis("off")

    plt.show()

    # print("Dataset local:", os.path.abspath(os.path.dirname(os.path.dirname(imagePath))))
    # print("Guardado:")
    # print("\t-", out1)
    # print("\t-", out2)
    # print("\t-", out3)


def main():
    datasetPath = downloadDatasetToProject()
    imgPath = pickNoisyImage(datasetPath, index=0)
    experimentA(imgPath, outDir=os.path.join(getProjectRoot(), "images"))


if __name__ == "__main__":
    main()

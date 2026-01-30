import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def loadGrayscaleImage(image_path: str) -> np.ndarray:
    """Carga una imagen en escala de grises (uint8)"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen: {image_path}")
    return img


def ensureBinaryImage(gray_img: np.ndarray) -> np.ndarray:
    """Convierte una imagen en escala de grises a binaria limpia con valores {0, 255} usando Otsu"""
    if gray_img.dtype != np.uint8:
        gray_img = gray_img.astype(np.uint8)

    _, binary = cv2.threshold(
        gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Forzar binario estricto por seguridad
    binary = np.where(binary > 0, 255, 0).astype(np.uint8)
    return binary


def normalizeForegroundToWhite(binary_img: np.ndarray) -> np.ndarray:
    """Asegura que las crestas de la huella sean el foreground"""
    white_ratio = float(np.mean(binary_img == 255))
    if white_ratio > 0.5:
        return cv2.bitwise_not(binary_img)
    return binary_img


def applyOpening(
    binary_img: np.ndarray,
    kernel_shape: int,
    kernel_size: int,
    iterations: int = 1
) -> np.ndarray:
    """Aplica apertura morfológica erosión -> dilatación"""
    kernel = cv2.getStructuringElement(
        kernel_shape, (kernel_size, kernel_size)
    )
    opened = cv2.morphologyEx(
        binary_img, cv2.MORPH_OPEN, kernel, iterations=iterations
    )
    return opened


def applyClosing(
    binary_img: np.ndarray,
    kernel_shape: int,
    kernel_size: int,
    iterations: int = 1
) -> np.ndarray:
    """Aplica cierre morfológico dilatación -> erosión"""
    kernel = cv2.getStructuringElement(
        kernel_shape, (kernel_size, kernel_size)
    )
    closed = cv2.morphologyEx(
        binary_img, cv2.MORPH_CLOSE, kernel, iterations=iterations
    )
    return closed


def showImages(
    images: list[np.ndarray],
    titles: list[str],
    figsize=(14, 6)
) -> None:
    plt.figure(figsize=figsize)
    for i, (img, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(img, cmap="gray", vmin=0, vmax=255)
        plt.title(title)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


def main() -> None:
    # 1. Ruta de la imagen de entrada
    image_path = "images/fingerprint_noisy.png"

    # 2. Carga y binarización
    gray_img = loadGrayscaleImage(image_path)
    binary_img = ensureBinaryImage(gray_img)
    binary_img = normalizeForegroundToWhite(binary_img)
    # print("Valores únicos en la imagen binaria:", np.unique(binary_img))

    # 3. Eliminación de ruido sal usando apertura
    open_kernel_shape = cv2.MORPH_ELLIPSE
    open_kernel_size = 3
    opened_img = applyOpening(
        binary_img,
        open_kernel_shape,
        open_kernel_size,
        iterations=1
    )

    # 4. Conexión de grietas usando cierre
    close_kernel_shape = cv2.MORPH_ELLIPSE
    close_kernel_size = 5
    final_img = applyClosing(
        opened_img,
        close_kernel_shape,
        close_kernel_size,
        iterations=1
    )

    # 5. Visualización
    showImages(
        [binary_img, opened_img, final_img],
        [
            "Imagen original binaria",
            "Paso 2. Apertura (eliminación de ruido sal)",
            "Imagen final. Cierre (conexión de grietas)"
        ],
        figsize=(16, 6)
    )

    # 6. Demostración
    closed_first = applyClosing(
        binary_img,
        close_kernel_shape,
        close_kernel_size,
        iterations=1
    )
    reverse_final = applyOpening(
        closed_first,
        open_kernel_shape,
        open_kernel_size,
        iterations=1
    )

    showImages(
        [final_img, reverse_final],
        [
            "Apertura → Cierre",
            "Cierre → Apertura"
        ],
        figsize=(12, 5)
    )


if __name__ == "__main__":
    main()

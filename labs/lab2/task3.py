import cv2
import numpy as np
import matplotlib.pyplot as plt
from task2 import loadGrayscaleImage


def computeFFT(gray_img: np.ndarray) -> np.ndarray:
    """Calcula la FFT 2D y centra el espectro"""
    fft = np.fft.fft2(gray_img)
    fft_shifted = np.fft.fftshift(fft)
    return fft_shifted


def applyLowPassFilter(
    fft_shifted: np.ndarray,
    radius: int
) -> np.ndarray:
    """Aplica un filtro paso bajo en el dominio de la frecuencia"""
    rows, cols = fft_shifted.shape
    center_row, center_col = rows // 2, cols // 2

    mask = np.zeros((rows, cols), dtype=np.uint8)
    cv2.circle(
        mask,
        (center_col, center_row),
        radius,
        1,
        thickness=-1
    )

    filtered_fft = fft_shifted * mask
    return filtered_fft


def computeIFFT(filtered_fft: np.ndarray) -> np.ndarray:
    """Calcula la IFFT y devuelve la imagen real normalizada"""
    ifft_shifted = np.fft.ifftshift(filtered_fft)
    img_back = np.fft.ifft2(ifft_shifted)
    img_back = np.abs(img_back)

    img_back = cv2.normalize(
        img_back, None, 0, 255, cv2.NORM_MINMAX
    ).astype(np.uint8)

    return img_back


def thresholdImage(
    img: np.ndarray,
    thresh_value: int
) -> np.ndarray:
    """Aplica umbralizado binario"""
    _, binary = cv2.threshold(
        img, thresh_value, 255, cv2.THRESH_BINARY
    )
    return binary


def refineMask(binary_img: np.ndarray) -> np.ndarray:
    """Limpia la máscara usando operaciones morfológicas"""
    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (3, 3)
    )
    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (5, 5)
    )

    opened = cv2.morphologyEx(
        binary_img, cv2.MORPH_OPEN, kernel_open
    )
    refined = cv2.morphologyEx(
        opened, cv2.MORPH_CLOSE, kernel_close
    )

    return refined


def showImages(
    images: list[np.ndarray],
    titles: list[str],
    figsize=(16, 8)
) -> None:
    plt.figure(figsize=figsize)
    for i, (img, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(1, len(images), i)
        plt.imshow(img, cmap="gray")
        plt.title(title)
        plt.axis("off")
    plt.tight_layout()
    plt.show()


def main() -> None:
    # 1. Carga de imagen
    image_path = "images/denim_tear.png"
    gray_img = loadGrayscaleImage(image_path)

    # 2. FFT y análisis en frecuencia
    fft_shifted = computeFFT(gray_img)
    magnitude_spectrum = np.log(1 + np.abs(fft_shifted))

    # 3. Filtrado en frecuencia
    filtered_fft = applyLowPassFilter(
        fft_shifted,
        radius=40
    )

    # 4. IFFT para volver al dominio espacial
    smoothed_img = computeIFFT(filtered_fft)

    # 5. Umbralizado para segmentación
    binary_mask = thresholdImage(
        smoothed_img,
        thresh_value=140
    )

    # 6. Refinamiento morfológico
    final_mask = refineMask(binary_mask)

    # 7. Visualización del pipeline
    showImages(
        [
            gray_img,
            magnitude_spectrum,
            smoothed_img,
            binary_mask,
            final_mask
        ],
        [
            "Imagen original",
            "Espectro de magnitud (FFT)",
            "Imagen suavizada (IFFT)",
            "Máscara preliminar (threshold)",
            "Máscara final (morfología)"
        ]
    )


if __name__ == "__main__":
    main()

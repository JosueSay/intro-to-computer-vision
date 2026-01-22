import cv2
import matplotlib.pyplot as plt
import numpy as np
import os


def normalizeTo255(img):
    """
    Normaliza una matriz a rango [0, 255] para visualización.
    """
    img = img.astype(np.float32, copy=False)
    mn = float(np.min(img))
    mx = float(np.max(img))
    if mx - mn < 1e-12:
        return np.zeros_like(img, dtype=np.float32)
    return (img - mn) * (255.0 / (mx - mn))


def toGray(imagen):
    """
    Convierte a grayscale si viene en BGR; si ya es 2D, retorna igual.
    """
    if imagen is None:
        raise ValueError("Imagen es None (ruta inválida o archivo no encontrado).")
    if imagen.ndim == 2:
        return imagen
    if imagen.ndim == 3 and imagen.shape[2] == 3:
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    raise ValueError(f"Formato de imagen no soportado: shape={imagen.shape}")


def manualPad(imagen, pad_h, pad_w, padding_type):

    if pad_h < 0 or pad_w < 0:
        raise ValueError("pad_h y pad_w deben ser >= 0")

    mode_map = {
        "reflect": ("reflect", None),
        "replicate": ("edge", None),
        "wrap": ("wrap", None),
        "zero": ("constant", 0),
    }
    if padding_type not in mode_map:
        raise ValueError("padding_type debe ser: 'reflect' | 'replicate' | 'wrap' | 'zero'")

    mode, cval = mode_map[padding_type]
    pad_width = ((pad_h, pad_h), (pad_w, pad_w))

    if mode == "constant":
        return np.pad(imagen, pad_width, mode=mode, constant_values=cval)
    return np.pad(imagen, pad_width, mode=mode)


def mi_convolucion(imagen, kernel, padding_type='reflect'):
    """
    Aplica convolución 2D a una imagen en escala de grises con padding manual.

    Args:
        imagen (np.ndarray): Imagen 2D (H, W) en escala de grises.
        kernel (np.ndarray): Kernel 2D (kH, kW).
        padding_type (str): 'reflect' | 'replicate' | 'wrap' | 'zero'.

    Returns:
        np.ndarray: Imagen filtrada (H, W).
    """
    if not isinstance(imagen, np.ndarray) or imagen.ndim != 2:
        raise ValueError("mi_convolucion: 'imagen' debe ser np.ndarray 2D (grayscale).")
    if not isinstance(kernel, np.ndarray) or kernel.ndim != 2:
        raise ValueError("mi_convolucion: 'kernel' debe ser np.ndarray 2D.")
    kH, kW = kernel.shape
    if kH < 1 or kW < 1:
        raise ValueError("mi_convolucion: kernel inválido.")
    if (kH % 2 == 0) or (kW % 2 == 0):
        # centralidad
        raise ValueError("mi_convolucion: se recomienda kernel de tamaño impar (kH y kW impares).")

    # Flip del kernel (convolución real)
    k = np.flip(kernel, axis=(0, 1)).astype(np.float32)

    pad_h = kH // 2
    pad_w = kW // 2

    img = imagen.astype(np.float32, copy=False)
    padded = manualPad(img, pad_h, pad_w, padding_type)

    # Ventanas (H, W, kH, kW)
    try:
        windows = np.lib.stride_tricks.sliding_window_view(padded, (kH, kW))
    except AttributeError as e:
        raise RuntimeError(
            "Tu NumPy no tiene sliding_window_view. Actualiza NumPy o implementa ventanas con stride_tricks."
        ) from e

    # windows: (H, W, kH, kW)  y  k: (kH, kW)
    out = np.einsum("ij,xyij->xy", k, windows, optimize=True)
    return out.astype(np.float32)


def generar_gaussiano(tamano, sigma):
    """
    Genera un kernel Gaussiano 2D centrado y normalizado.

    Args:
        tamano (int): Tamaño del kernel (tamano x tamano), idealmente impar.
        sigma (float): Desviación estándar del Gaussiano.

    Returns:
        np.ndarray: Kernel Gaussiano 2D normalizado (suma = 1.0).
    """
    # TODO: Validar tamano (entero > 0) y sigma (> 0)
    # TODO: Crear grilla centrada (coordenadas)
    # TODO: Evaluar Gaussiana 2D
    # TODO: Normalizar para que la suma sea 1.0
    raise NotImplementedError


def detectar_bordes_sobel(imagen):
    """
    Calcula bordes usando Sobel: magnitud y dirección del gradiente.

    Args:
        imagen (np.ndarray): Imagen 2D (H, W) en escala de grises.

    Returns:
        tuple[np.ndarray, np.ndarray]:
            - G (np.ndarray): Magnitud normalizada a 0-255 (float o uint8).
            - theta (np.ndarray): Dirección del gradiente (radianes o grados).
    """
    # TODO: Validar grayscale
    # TODO: Definir kernels Sobel Gx y Gy (3x3)
    # TODO: Aplicar mi_convolucion para obtener gradientes Gx_img y Gy_img
    # TODO: Calcular magnitud: sqrt(Gx^2 + Gy^2)
    # TODO: Normalizar magnitud a 0-255 para visualización
    # TODO: Calcular dirección: arctan2(Gy, Gx)
    # TODO: Retornar (G, theta)
    raise NotImplementedError


def main():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img1_path = os.path.join(base_dir, "images", "task2.use-image1.png")
    img2_path = os.path.join(base_dir, "images", "task2.use-image2.jpg")

    paths = [img1_path, img2_path]


if __name__ == "__main__":
    main()

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
    if not isinstance(tamano, int) or tamano <= 0:
        raise ValueError("generar_gaussiano: 'tamano' debe ser entero > 0.")
    if tamano % 2 == 0:
        raise ValueError("generar_gaussiano: 'tamano' debe ser impar para centrar el kernel.")
    if not (isinstance(sigma, (int, float)) and sigma > 0):
        raise ValueError("generar_gaussiano: 'sigma' debe ser > 0.")

    r = tamano // 2
    ax = np.arange(-r, r + 1, dtype=np.float32)
    xx, yy = np.meshgrid(ax, ax)

    gauss = np.exp(-(xx**2 + yy**2) / (2.0 * (sigma**2)))
    s = float(np.sum(gauss))
    if s <= 0:
        raise ValueError("generar_gaussiano: suma inválida del kernel.")
    gauss /= s
    return gauss.astype(np.float32)


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
    if not isinstance(imagen, np.ndarray) or imagen.ndim != 2:
        raise ValueError("detectar_bordes_sobel: 'imagen' debe ser np.ndarray 2D (grayscale).")

    # Kernels Sobel clásicos (3x3)
    Gx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]], dtype=np.float32)

    Gy = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]], dtype=np.float32)

    gx_img = mi_convolucion(imagen, Gx, padding_type="reflect")
    gy_img = mi_convolucion(imagen, Gy, padding_type="reflect")

    mag = np.sqrt(gx_img**2 + gy_img**2).astype(np.float32)
    G = normalizeTo255(mag)

    theta = np.arctan2(gy_img, gx_img).astype(np.float32)  # radianes [-pi, pi]
    return G, theta


def main():
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img1_path = os.path.join(base_dir, "images", "task2.use-image1.png")
    img2_path = os.path.join(base_dir, "images", "task2.use-image2.jpg")

    paths = [img1_path, img2_path]

    for p in paths:
        bgr = cv2.imread(p, cv2.IMREAD_COLOR)
        gray = toGray(bgr)

        k_gauss = generar_gaussiano(tamano=5, sigma=1.0)
        gray_smooth = mi_convolucion(gray, k_gauss, padding_type="reflect")

        G_raw, theta_raw = detectar_bordes_sobel(gray)
        G_smooth, theta_smooth = detectar_bordes_sobel(gray_smooth)

        # Visualización
        fig, axs = plt.subplots(
            2, 3,
            figsize=(16, 8),
            gridspec_kw={"hspace": 0.35, "wspace": 0.15}
        )

        fig.canvas.manager.set_window_title(
            f"Procedimiento -s {os.path.basename(p)}"
        )

        # Fila 1: sin suavizado
        axs[0, 0].imshow(gray, cmap="gray")
        axs[0, 0].set_title("Gray (original)")
        axs[0, 0].axis("off")

        axs[0, 1].imshow(G_raw, cmap="gray")
        axs[0, 1].set_title("Sobel |G| (raw)")
        axs[0, 1].axis("off")

        axs[0, 2].imshow(theta_raw, cmap="gray")
        axs[0, 2].set_title("Dirección theta (raw)")
        axs[0, 2].axis("off")

        # Fila 2: con suavizado
        axs[1, 0].imshow(gray_smooth, cmap="gray")
        axs[1, 0].set_title("Gray (Gauss 5x5, sigma=1)")
        axs[1, 0].axis("off")

        axs[1, 1].imshow(G_smooth, cmap="gray")
        axs[1, 1].set_title("Sobel |G| (smooth)")
        axs[1, 1].axis("off")

        axs[1, 2].imshow(theta_smooth, cmap="gray")
        axs[1, 2].set_title("Dirección theta (smooth)")
        axs[1, 2].axis("off")

        plt.show()
        

if __name__ == "__main__":
    main()

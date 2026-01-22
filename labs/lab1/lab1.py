import numpy as np
import cv2
import matplotlib.pyplot as plt


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
    # TODO: Validar que imagen sea 2D (grayscale)
    # TODO: Validar kernel 2D y tamaño impar recomendado
    # TODO: Flip del kernel (convolución) antes de aplicar
    # TODO: Padding manual según padding_type
    # TODO: Convolución optimizada (evitar 4 for; usar slicing / einsum o 2 for)
    # TODO: Retornar resultado con tipo adecuado
    raise NotImplementedError


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


def manualPad(imagen, pad_h, pad_w, padding_type):
    """
    Padding manual (camelCase para diferenciar).
    """
    # TODO: Implementar zero/reflect/replicate/wrap sin usar cv2.copyMakeBorder
    raise NotImplementedError


def normalizeTo255(img):
    """
    Normaliza una matriz a rango [0, 255] para visualización.
    """
    # TODO: Implementar normalización robusta (manejar max==min)
    raise NotImplementedError


def toGray(imagen):
    """
    Convierte a grayscale si viene en BGR; si ya es 2D, retorna igual.
    """
    # TODO: Si imagen tiene 3 canales, convertir a gris (permitido con cv2.cvtColor)
    raise NotImplementedError


def main():
    """
    Punto de entrada para pruebas locales.
    """
    # TODO: Cargar imagen con cv2.imread
    # TODO: Convertir a gris (si aplica)
    # TODO: Generar kernel Gaussiano y filtrar con mi_convolucion (si quieres probar)
    # TODO: Ejecutar detectar_bordes_sobel
    # TODO: Visualizar con matplotlib
    raise NotImplementedError


if __name__ == "__main__":
    main()

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Inciso 1: Cargar imagen
img = cv2.imread('images/periodic_noise.jpg', cv2.IMREAD_GRAYSCALE)

plt.figure(figsize=(5,5))
plt.imshow(img, cmap='gray')
plt.title('Imagen original con ruido periódico')
plt.axis('off')
plt.savefig('images/task1_original.png', bbox_inches='tight')
plt.close()

# Inciso 2: DFT y centrado
dft = np.fft.fft2(img)
dft_shift = np.fft.fftshift(dft)

# Inciso 3: Espectro de magnitud
magnitude_spectrum = 20 * np.log(np.abs(dft_shift) + 1)

plt.figure(figsize=(5,5))
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Espectro de Magnitud (escala logarítmica)')
plt.axis('off')
plt.savefig('images/task1_magnitude_spectrum.png', bbox_inches='tight')
plt.close()

# Inciso 4: Marcar picos de ruido
spectrum_marked = cv2.cvtColor(
    cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
    cv2.COLOR_GRAY2BGR
)

rows, cols = img.shape

notches = [
    (rows//2 + 30, cols//2 + 60),
    (rows//2 - 30, cols//2 - 60),
    (rows//2 + 30, cols//2 - 60),
    (rows//2 - 30, cols//2 + 60)
]

for r, c in notches:
    cv2.circle(spectrum_marked, (c, r), 8, (0, 0, 255), 2)

plt.figure(figsize=(5,5))
plt.imshow(spectrum_marked)
plt.title('Picos de ruido identificados')
plt.axis('off')
plt.savefig('images/task1_magnitude_peaks.png', bbox_inches='tight')
plt.close()

# Inciso 5: Notch Filter
mask = np.ones((rows, cols), np.uint8)

for r, c in notches:
    cv2.circle(mask, (c, r), 6, 0, -1)

filtered_dft = dft_shift * mask

plt.figure(figsize=(5,5))
plt.imshow(mask, cmap='gray')
plt.title('Máscara Notch Filter')
plt.axis('off')
plt.savefig('images/task1_notch_mask.png', bbox_inches='tight')
plt.close()

# Inciso 6: IDFT
idft_shift = np.fft.ifftshift(filtered_dft)
img_restored = np.fft.ifft2(idft_shift)
img_restored = np.abs(img_restored)

plt.figure(figsize=(5,5))
plt.imshow(img_restored, cmap='gray')
plt.title('Imagen restaurada sin ruido periódico')
plt.axis('off')
plt.savefig('images/task1_restored.png', bbox_inches='tight')
plt.close()

print("Task 1 completado. Imágenes guardadas en /images")

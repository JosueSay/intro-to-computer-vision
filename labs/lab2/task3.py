import os
from datetime import datetime

import cv2
import numpy as np
import matplotlib.pyplot as plt
from task2 import loadGrayscaleImage


LOG_DIR = "logs"
CSV_DIR = "csv"
CSV_HEADER = [
	"timestamp",
	"image_name",
	"pipeline",
	"img_h",
	"img_w",
	"sigma",
	"radius",
	"p_used",
	"thr_used",
	"white_ratio_raw",
	"white_ratio_pre",
	"white_ratio_candidate",
	"white_ratio_final",
	"candidate_area",
	"candidate_energy_sum",
	"candidate_bbox_x",
	"candidate_bbox_y",
	"candidate_bbox_w",
	"candidate_bbox_h",
]


"""
Formato de logs (TSV):
1. timestamp_utc,LEVEL,STAGE,message,k=v,k=v...
"""
def ensure_dirs() -> None:
	os.makedirs(LOG_DIR, exist_ok=True)
	os.makedirs(CSV_DIR, exist_ok=True)


def utc_ts() -> str:
	return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def file_ts() -> str:
	return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def open_log_and_csv(run_name: str) -> tuple[str, str]:
	ensure_dirs()
	log_path = os.path.join(LOG_DIR, f"{run_name}.log")
	csv_path = os.path.join(CSV_DIR, f"{run_name}.csv")

	with open(csv_path, "w", encoding="utf-8", newline="\n") as f:
		f.write(",".join(CSV_HEADER) + "\n")

	return log_path, csv_path


def log_event(log_path: str, level: str, stage: str, msg: str, **kv: object) -> None:
	parts = [utc_ts(), level, stage, msg]
	for k, v in kv.items():
		parts.append(f"{k}={v}")
	line = "\t".join(parts) + "\n"
	print(line, end="")
	with open(log_path, "a", encoding="utf-8", newline="\n") as f:
		f.write(line)


def csv_append(csv_path: str, row: dict[str, object]) -> None:
	values = []
	for k in CSV_HEADER:
		values.append(str(row.get(k, "")))
	line = ",".join(values) + "\n"
	with open(csv_path, "a", encoding="utf-8", newline="\n") as f:
		f.write(line)


def img_stats(img: np.ndarray) -> dict[str, float]:
	vals = img.astype(np.float32)
	return {
		"min": float(np.min(vals)),
		"p1": float(np.percentile(vals, 1)),
		"p5": float(np.percentile(vals, 5)),
		"p50": float(np.percentile(vals, 50)),
		"p95": float(np.percentile(vals, 95)),
		"p99": float(np.percentile(vals, 99)),
		"max": float(np.max(vals)),
		"mean": float(np.mean(vals)),
		"std": float(np.std(vals)),
	}


"""
Connected Components (CC):
1. Reporta los componentes por área (topk) y métricas para depurar
2. Distancia al centro ayuda cuando el defecto suele estar cerca del centro
3. touches_border evita que el fondo pegado al borde “gane” por área
"""

def cc_report(binary: np.ndarray, topk: int = 10) -> list[dict[str, object]]:
	num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
	h, w = binary.shape
	cx0, cy0 = w / 2.0, h / 2.0

	rows: list[dict[str, object]] = []
	for lab in range(1, num_labels):
		x = int(stats[lab, cv2.CC_STAT_LEFT])
		y = int(stats[lab, cv2.CC_STAT_TOP])
		ww = int(stats[lab, cv2.CC_STAT_WIDTH])
		hh = int(stats[lab, cv2.CC_STAT_HEIGHT])
		area = int(stats[lab, cv2.CC_STAT_AREA])

		cx, cy = centroids[lab]
		dist = float(np.sqrt((cx - cx0) ** 2 + (cy - cy0) ** 2))
		aspect = float(max(ww, hh) / max(1, min(ww, hh)))
		touches_border = (x == 0) or (y == 0) or (x + ww >= w) or (y + hh >= h)

		rows.append(
			{
				"label": lab,
				"area": area,
				"dist": dist,
				"aspect": aspect,
				"touches_border": touches_border,
				"bbox": (x, y, ww, hh),
			}
		)

	rows.sort(key=lambda r: int(r["area"]), reverse=True)
	return rows[:topk]


def show_images(images: list[np.ndarray], titles: list[str], figsize=(16, 8)) -> None:
	plt.figure(figsize=figsize)
	for i, (img, title) in enumerate(zip(images, titles), start=1):
		plt.subplot(1, len(images), i)
		plt.imshow(img, cmap="gray", vmin=0, vmax=255)
		plt.title(title)
		plt.axis("off")
	plt.tight_layout()
	plt.show()


def ComputeFFT(gray_img: np.ndarray) -> np.ndarray:
	fft = np.fft.fft2(gray_img)
	return np.fft.fftshift(fft)


def ComputeIFFT(filtered_fft: np.ndarray) -> np.ndarray:
	ifft_shifted = np.fft.ifftshift(filtered_fft)
	img_back = np.fft.ifft2(ifft_shifted)
	img_back = np.abs(img_back)
	return cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


def ApplyLowPassFilter(fft_shifted: np.ndarray, radius: int) -> np.ndarray:
	rows, cols = fft_shifted.shape
	center_row, center_col = rows // 2, cols // 2
	mask = np.zeros((rows, cols), dtype=np.uint8)
	cv2.circle(mask, (center_col, center_row), radius, 1, thickness=-1)
	return fft_shifted * mask


def ApplyGaussianLowPassFilter(fft_shifted: np.ndarray, sigma: float) -> tuple[np.ndarray, np.ndarray]:
	rows, cols = fft_shifted.shape
	center_row, center_col = rows // 2, cols // 2

	y, x = np.ogrid[:rows, :cols]
	dist2 = (y - center_row) ** 2 + (x - center_col) ** 2
	mask = np.exp(-dist2 / (2.0 * (sigma ** 2))).astype(np.float32)

	return fft_shifted * mask, mask


def threshold_image(img: np.ndarray, thresh_value: int) -> np.ndarray:
	_, binary = cv2.threshold(img, thresh_value, 255, cv2.THRESH_BINARY)
	return binary


"""
Morfología:
1. OPEN quita ruido blanco pequeño
2. CLOSE rellena huecos y conecta partes cercanas del defecto
3. Tamaños de kernel ajustables si cambia la escala del defecto
"""

def refine_mask(binary_img: np.ndarray) -> np.ndarray:
	kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
	opened = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel_open)
	refined = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
	return refined


def threshold_by_percentile(img: np.ndarray, percentile: float) -> tuple[np.ndarray, float]:
	t = float(np.percentile(img, percentile))
	_, binary = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
	return binary, t


"""
Selección de umbral por percentiles:
1. Evita Otsu cuando el fondo domina 
2. Busca un white_ratio para que CC tenga algo que escoger
3. min_thr evita el caso común thr=0 cuando casi todo es 0
"""

def choose_percentile_threshold(
	img: np.ndarray,
	p_list: list[float],
	min_thr: float,
	target_white_min: float,
	target_white_max: float,
	log_path: str,
	stage: str,
) -> tuple[np.ndarray, float, float, float]:
	fallback = None
	in_range: list[tuple[np.ndarray, float, float, float]] = []

	for p in p_list:
		b, t = threshold_by_percentile(img, p)
		wr = float(np.mean(b == 255))
		log_event(log_path, "INFO", stage, "percentile_probe", p=p, thr=t, white_ratio=wr)

		if t >= min_thr and fallback is None:
			fallback = (b, p, t, wr)

		if t >= min_thr and (target_white_min <= wr <= target_white_max):
			in_range.append((b, p, t, wr))

	if in_range:
		in_range.sort(key=lambda x: x[1], reverse=True)
		b, p, t, wr = in_range[0]
		log_event(log_path, "INFO", stage, "percentile_select_in_range", p_used=p, thr_used=t, white_ratio_raw=wr)
		return b, t, p, wr

	if fallback is not None:
		b, p, t, wr = fallback
		log_event(log_path, "WARN", stage, "percentile_select_fallback", p_used=p, thr_used=t, white_ratio_raw=wr)
		return b, t, p, wr

	b, t = threshold_by_percentile(img, max(p_list))
	wr = float(np.mean(b == 255))
	log_event(log_path, "ERROR", stage, "percentile_select_forced", p_used=max(p_list), thr_used=t, white_ratio_raw=wr)
	return b, t, max(p_list), wr


"""
Selección de componente por energía:
1. En vez de “más grande” o “más centrado”, usa suma(energy_img) por componente
2. Aquí energy_img = diff_pos_blur, que resalta el defecto en textile_defect.jpg
3. reject_border evita que regiones grandes pegadas a bordes ganen
"""

def pick_component_by_energy(
	binary_img: np.ndarray,
	energy_img: np.ndarray,
	min_area: int,
	reject_border: bool,
) -> tuple[np.ndarray, dict[str, object] | None]:
	num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_img, connectivity=8)
	if num_labels <= 1:
		return binary_img, None

	h, w = binary_img.shape
	best_label = -1
	best_energy = -1.0
	best_info: dict[str, object] | None = None

	for lab in range(1, num_labels):
		x = int(stats[lab, cv2.CC_STAT_LEFT])
		y = int(stats[lab, cv2.CC_STAT_TOP])
		ww = int(stats[lab, cv2.CC_STAT_WIDTH])
		hh = int(stats[lab, cv2.CC_STAT_HEIGHT])
		area = int(stats[lab, cv2.CC_STAT_AREA])

		if area < min_area:
			continue

		touches_border = (x == 0) or (y == 0) or (x + ww >= w) or (y + hh >= h)
		if reject_border and touches_border:
			continue

		mask = labels == lab
		e_sum = float(np.sum(energy_img[mask]))

		if e_sum > best_energy:
			best_energy = e_sum
			best_label = lab
			best_info = {
				"label": lab,
				"area": area,
				"energy_sum": e_sum,
				"bbox": (x, y, ww, hh),
			}

	out = np.zeros_like(binary_img)
	if best_label != -1:
		out[labels == best_label] = 255
		return out, best_info

	return binary_img, None


def RunPipelineDenim(
	image_name: str,
	gray_img: np.ndarray,
	log_path: str,
	csv_path: str,
) -> None:
	radius = 40
	thresh_value = 140
	h, w = gray_img.shape

	log_event(log_path, "INFO", "denim", "start", image=image_name, radius=radius, thresh=thresh_value)

	fft_shifted = ComputeFFT(gray_img)
	magnitude_spectrum = np.log(1 + np.abs(fft_shifted))

	filtered_fft = ApplyLowPassFilter(fft_shifted, radius=radius)
	smoothed_img = ComputeIFFT(filtered_fft)

	binary_mask = threshold_image(smoothed_img, thresh_value=thresh_value)
	final_mask = refine_mask(binary_mask)

	wr_candidate = float(np.mean(binary_mask == 255))
	wr_final = float(np.mean(final_mask == 255))
	log_event(log_path, "INFO", "denim", "finish", white_ratio_candidate=wr_candidate, white_ratio_final=wr_final)

	csv_append(
		csv_path,
		{
			"timestamp": utc_ts(),
			"image_name": image_name,
			"pipeline": "denim",
			"img_h": h,
			"img_w": w,
			"sigma": "",
			"radius": radius,
			"p_used": "",
			"thr_used": thresh_value,
			"white_ratio_raw": "",
			"white_ratio_pre": "",
			"white_ratio_candidate": wr_candidate,
			"white_ratio_final": wr_final,
			"candidate_area": "",
			"candidate_energy_sum": "",
			"candidate_bbox_x": "",
			"candidate_bbox_y": "",
			"candidate_bbox_w": "",
			"candidate_bbox_h": "",
		},
	)

	show_images(
		[gray_img, magnitude_spectrum, smoothed_img, binary_mask, final_mask],
		[
			"Imagen original",
			"Espectro de magnitud (FFT)",
			"Imagen suavizada (IFFT)",
			"Máscara preliminar (threshold)",
			"Máscara final (morfología)",
		],
		figsize=(18, 6),
	)


def RunPipelineTextile(
	image_name: str,
	gray_img: np.ndarray,
	log_path: str,
	csv_path: str,
) -> None:
	sigma = 12.0
	h, w = gray_img.shape

	log_event(log_path, "INFO", "textile", "start", image=image_name, sigma=sigma)

	fft_shifted = ComputeFFT(gray_img)
	magnitude_spectrum = np.log(1 + np.abs(fft_shifted))
	magnitude_spectrum_vis = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

	filtered_fft, gaussian_mask = ApplyGaussianLowPassFilter(fft_shifted, sigma=sigma)
	gaussian_mask_vis = cv2.normalize(gaussian_mask, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

	smoothed_img = ComputeIFFT(filtered_fft)

	"""
	Diferencia dirigida (clave en textile_defect.jpg):
	1. absdiff mezclaba cambios en ambos sentidos (más oscuro y más claro).
	2. interesa solo donde la suavizada es más brillante que la original
	3. Eso separa mejor el defecto del grano del fondo
	"""
	diff_pos = np.clip(smoothed_img.astype(np.int16) - gray_img.astype(np.int16), 0, 255).astype(np.uint8)
	diff_pos_blur = cv2.GaussianBlur(diff_pos, (0, 0), sigmaX=2.0)
	diff_pos_blur_vis = cv2.normalize(diff_pos_blur, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

	s0 = img_stats(gray_img)
	s1 = img_stats(smoothed_img)
	s2 = img_stats(diff_pos)
	s3 = img_stats(diff_pos_blur)
	log_event(log_path, "INFO", "textile_stats", "gray_img", **s0)
	log_event(log_path, "INFO", "textile_stats", "smoothed_img", **s1)
	log_event(log_path, "INFO", "textile_stats", "diff_pos", **s2)
	log_event(log_path, "INFO", "textile_stats", "diff_pos_blur", **s3)

	p_list = [97.0, 97.5, 98.0, 98.5, 99.0, 99.2, 99.4, 99.6, 99.8, 99.9]
	binary_raw, thr_used, p_used, wr_raw = choose_percentile_threshold(
		diff_pos_blur,
		p_list=p_list,
		min_thr=1.0,
		target_white_min=0.001,
		target_white_max=0.02,
		log_path=log_path,
		stage="textile_percentile",
	)

	kernel_pre = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
	binary_pre = cv2.morphologyEx(binary_raw, cv2.MORPH_OPEN, kernel_pre, iterations=1)
	wr_pre = float(np.mean(binary_pre == 255))
	log_event(log_path, "INFO", "textile", "pre_open", white_ratio_pre=wr_pre)

	top_raw = cc_report(binary_raw, topk=10)
	top_pre = cc_report(binary_pre, topk=10)
	for r in top_raw:
		x, y, ww, hh = r["bbox"]
		log_event(
			log_path,
			"INFO",
			"textile_cc_raw",
			"cc",
			label=r["label"],
			area=r["area"],
			dist=r["dist"],
			aspect=r["aspect"],
			touches_border=r["touches_border"],
			bbox_x=x,
			bbox_y=y,
			bbox_w=ww,
			bbox_h=hh,
		)
	for r in top_pre:
		x, y, ww, hh = r["bbox"]
		log_event(
			log_path,
			"INFO",
			"textile_cc_pre",
			"cc",
			label=r["label"],
			area=r["area"],
			dist=r["dist"],
			aspect=r["aspect"],
			touches_border=r["touches_border"],
			bbox_x=x,
			bbox_y=y,
			bbox_w=ww,
			bbox_h=hh,
		)

	binary_mask, best_info = pick_component_by_energy(
		binary_pre,
		energy_img=diff_pos_blur,
		min_area=50,
		reject_border=True,
	)

	wr_candidate = float(np.mean(binary_mask == 255))
	log_event(log_path, "INFO", "textile", "candidate", white_ratio_candidate=wr_candidate)

	final_mask = refine_mask(binary_mask)
	wr_final = float(np.mean(final_mask == 255))
	log_event(log_path, "INFO", "textile", "finish", white_ratio_final=wr_final)

	bx = by = bw = bh = area = e_sum = ""
	if best_info is not None:
		area = best_info["area"]
		e_sum = best_info["energy_sum"]
		bx, by, bw, bh = best_info["bbox"]
		log_event(
			log_path,
			"INFO",
			"textile_pick",
			"picked_by_energy",
			area=area,
			energy_sum=e_sum,
			bbox_x=bx,
			bbox_y=by,
			bbox_w=bw,
			bbox_h=bh,
		)
	else:
		log_event(log_path, "WARN", "textile_pick", "no_valid_component")

	csv_append(
		csv_path,
		{
			"timestamp": utc_ts(),
			"image_name": image_name,
			"pipeline": "textile",
			"img_h": h,
			"img_w": w,
			"sigma": sigma,
			"radius": "",
			"p_used": p_used,
			"thr_used": thr_used,
			"white_ratio_raw": wr_raw,
			"white_ratio_pre": wr_pre,
			"white_ratio_candidate": wr_candidate,
			"white_ratio_final": wr_final,
			"candidate_area": area,
			"candidate_energy_sum": e_sum,
			"candidate_bbox_x": bx,
			"candidate_bbox_y": by,
			"candidate_bbox_w": bw,
			"candidate_bbox_h": bh,
		},
	)

	show_images(
		[
			gray_img,
			magnitude_spectrum_vis,
			gaussian_mask_vis,
			smoothed_img,
			diff_pos_blur_vis,
			binary_raw,
			binary_pre,
			binary_mask,
			final_mask,
		],
		[
			"Imagen original",
			"Espectro de magnitud (FFT)",
			"Máscara paso bajo gaussiana (frecuencia)",
			"Imagen suavizada (IFFT)",
			"diff_pos_blur (visualizado con normalize)",
			"Máscara raw (percentil)",
			"Máscara tras apertura 3x3",
			"Candidato (CC por energía)",
			"Máscara final (morfología)",
		],
		figsize=(28, 7),
	)


def main() -> None:
	run_name = f"task3_{file_ts()}"
	log_path, csv_path = open_log_and_csv(run_name)
	log_event(log_path, "INFO", "run", "start", run_name=run_name, csv_path=csv_path)

	"""
	1. Cada imagen corre con su pipeline específico
	2. Los resultados quedan en un único log/csv por corrida (timestamped)
	"""
	images = [
		("images/denim_tear.png", "denim"),
		("images/textile_defect.jpg", "textile"),
	]

	for image_path, pipeline in images:
		image_name = os.path.basename(image_path)
		gray_img = loadGrayscaleImage(image_path)
		log_event(log_path, "INFO", "run", "image_loaded", image=image_name, pipeline=pipeline, shape=str(gray_img.shape))

		if pipeline == "denim":
			RunPipelineDenim(image_name, gray_img, log_path, csv_path)
		else:
			RunPipelineTextile(image_name, gray_img, log_path, csv_path)

	log_event(log_path, "INFO", "run", "finish", run_name=run_name)


if __name__ == "__main__":
	main()

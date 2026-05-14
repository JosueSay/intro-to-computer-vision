"""
Intercepcion del proceso de denoising en Stable Diffusion 1.5 para observar
la evolucion del tensor latente en los pasos 4, 10, 16 y 20 de un total de 20.

Pipeline general:
1. Carga StableDiffusionPipeline (SD 1.5) en GPU.
2. Programa el scheduler para 20 pasos de inferencia.
3. Durante el loop de denoising, intercepta el latente via callback_on_step_end y guarda copias en los pasos seleccionados.
4. Al terminar, decodifica manualmente cada latente con vae.decode(), aplicando la division por vae.config.scaling_factor.
5. Guarda cada imagen individual y una cuadricula 2x2 con las cuatro etapas.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont

PROMPT = (
    "A highly detailed cinematic and futuristic fruit glowing in a "
    "cyberpunk laboratory, neon lights, 4k resolution"
)

CAPTURE_STEPS = {4, 10, 16, 20}
TOTAL_STEPS = 20
DEFAULT_SEED = 42
DEFAULT_MODEL = "stable-diffusion-v1-5/stable-diffusion-v1-5"


def build_pipeline(model_id: str, device: str) -> StableDiffusionPipeline:
    """Carga el pipeline de Stable Diffusion en el device indicado."""
    dtype = torch.float16 if device == "cuda" else torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
    pipe = pipe.to(device)
    pipe.set_progress_bar_config(disable=False)
    return pipe


def make_capture_callback(captured: dict[int, torch.Tensor]):
    """Construye el callback que diffusers invoca al final de cada paso.

    Diffusers numera los pasos desde 0, por eso convertimos a base 1 antes
    de comparar contra CAPTURE_STEPS.
    """

    def callback(pipe, step_index: int, timestep: int, callback_kwargs: dict):
        human_step = step_index + 1
        if human_step in CAPTURE_STEPS:
            latents = callback_kwargs["latents"].detach().clone()
            captured[human_step] = latents
        return callback_kwargs

    return callback


def decode_latent(pipe: StableDiffusionPipeline, latent: torch.Tensor) -> Image.Image:
    """Decodifica un latente intermedio a una imagen PIL.

    El VAE de SD trabaja con latentes escalados por scaling_factor.
    Durante el denoising los latentes viven en el espacio
    escalado, asi que antes de pasar por vae.decode hay que dividir por ese
    factor para devolverlos al rango esperado por el decoder.
    """
    vae = pipe.vae
    latent = latent.to(device=vae.device, dtype=vae.dtype)
    latent = latent / vae.config.scaling_factor

    with torch.no_grad():
        decoded = vae.decode(latent).sample

    decoded = (decoded / 2 + 0.5).clamp(0, 1)
    array = decoded.squeeze(0).permute(1, 2, 0).float().cpu().numpy()
    array = (array * 255).round().astype("uint8")
    return Image.fromarray(array)


def build_grid(images: dict[int, Image.Image]) -> Image.Image:
    """Arma una cuadricula 2x2 con etiqueta de paso sobre cada imagen."""
    ordered_steps = sorted(images.keys())
    cell_w, cell_h = images[ordered_steps[0]].size
    label_h = 32
    grid = Image.new("RGB", (cell_w * 2, (cell_h + label_h) * 2), color=(15, 15, 15))
    draw = ImageDraw.Draw(grid)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()

    for idx, step in enumerate(ordered_steps):
        row, col = divmod(idx, 2)
        x = col * cell_w
        y = row * (cell_h + label_h)
        draw.text((x + 12, y + 4), f"Paso {step}/{TOTAL_STEPS}", fill="white", font=font)
        grid.paste(images[step], (x, y + label_h))

    return grid


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("[advertencia] CUDA no disponible, se ejecutara en CPU (muy lento).")

    print(f"[info] Cargando modelo {args.model} en {device}...")
    pipe = build_pipeline(args.model, device)

    generator = torch.Generator(device=device).manual_seed(args.seed)
    torch.manual_seed(args.seed)

    captured: dict[int, torch.Tensor] = {}
    callback = make_capture_callback(captured)

    print(f"[info] Generando con prompt:\n  {PROMPT}")
    pipe(
        prompt=PROMPT,
        num_inference_steps=TOTAL_STEPS,
        generator=generator,
        callback_on_step_end=callback,
        callback_on_step_end_tensor_inputs=["latents"],
    )

    missing = CAPTURE_STEPS - captured.keys()
    if missing:
        raise RuntimeError(f"No se capturaron los pasos esperados: {sorted(missing)}")

    print("[info] Decodificando latentes capturados...")
    images: dict[int, Image.Image] = {}
    for step in sorted(CAPTURE_STEPS):
        image = decode_latent(pipe, captured[step])
        out_path = args.output_dir / f"step_{step:02d}.png"
        image.save(out_path)
        images[step] = image
        print(f"\t- guardado {out_path}")

    grid = build_grid(images)
    grid_path = args.output_dir / "grid.png"
    grid.save(grid_path)
    print(f"[ok] Cuadricula final en {grid_path}")


if __name__ == "__main__":
    main()

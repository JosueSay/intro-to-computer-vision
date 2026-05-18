import time
import torch
from diffusers import StableDiffusionPipeline, LCMScheduler
from PIL import Image
import gc
import os

# Fix for RTX 50 series (Blackwell) kernel architecture mismatch
torch.backends.cuda.enable_flash_sdp(False)
torch.backends.cuda.enable_mem_efficient_sdp(False)
torch.backends.cuda.enable_math_sdp(True)

PROMPT = "A highly detailed cinematic and futuristic fruit glowing in a cyberpunk laboratory, neon lights, 4k resolution"
SEED = 42

def flush():
    gc.collect()
    torch.cuda.empty_cache()
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()

def run_standard():
    flush()
    print("--- Escenario A: Modelo Estandar ---")
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", 
        torch_dtype=torch.float16
    ).to("cuda")
    
    generator = torch.Generator("cuda").manual_seed(SEED)
    
    torch.cuda.reset_peak_memory_stats()
    start_time = time.time()
    image = pipe(
        prompt=PROMPT, 
        num_inference_steps=50, 
        generator=generator
    ).images[0]
    end_time = time.time()
    
    time_taken = end_time - start_time
    max_vram = torch.cuda.max_memory_allocated() / (1024 ** 2) # en MB
    
    print(f"Tiempo: {time_taken:.2f} s")
    print(f"VRAM Peak: {max_vram:.2f} MB")
    
    image.save("outputs/task2_standard.png")
    
    del pipe
    flush()
    return time_taken, max_vram

def run_distilled():
    flush()
    print("--- Escenario B: Modelo Destilado (SD-Turbo) ---")
    from diffusers import AutoPipelineForText2Image
    
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sd-turbo", 
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")
    
    generator = torch.Generator("cuda").manual_seed(SEED)
    
    torch.cuda.reset_peak_memory_stats()
    start_time = time.time()
    # SD-Turbo uses guidance_scale=0.0 and 1-4 steps
    image = pipe(
        prompt=PROMPT, 
        num_inference_steps=4, 
        guidance_scale=0.0,
        generator=generator
    ).images[0]
    end_time = time.time()
    
    time_taken = end_time - start_time
    max_vram = torch.cuda.max_memory_allocated() / (1024 ** 2) # en MB
    
    print(f"Tiempo: {time_taken:.2f} s")
    print(f"VRAM Peak: {max_vram:.2f} MB")
    
    image.save("outputs/task2_distilled.png")
    
    del pipe
    flush()
    return time_taken, max_vram

def main():
    os.makedirs("outputs", exist_ok=True)
    
    t1, vram1 = run_standard()
    t2, vram2 = run_distilled()
    
    img1 = Image.open("outputs/task2_standard.png")
    img2 = Image.open("outputs/task2_distilled.png")
    
    w, h = img1.size
    combined = Image.new("RGB", (w * 2, h))
    combined.paste(img1, (0, 0))
    # resize img2 if needed to match img1 height
    if img2.size[1] != h:
        img2 = img2.resize((int(img2.size[0] * h / img2.size[1]), h))
    combined.paste(img2, (w, 0))
    combined.save("outputs/task2_comparison.png")
    
    print("\n--- Resultados ---")
    print(f"Estandar  (50 pasos): {t1:.2f} s, {vram1:.2f} MB")
    print(f"Destilado ( 4 pasos): {t2:.2f} s, {vram2:.2f} MB")

if __name__ == "__main__":
    main()

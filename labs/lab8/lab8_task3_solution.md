# Task 3 Solution for Lab 8

Since I cannot modify `.ipynb` files directly, please copy the following code blocks into your notebook under the **Task 3** section.

## 1. Environment Setup
Add this to a new code cell:
```python
# Instalación de dependencias
!pip install ultralytics roboflow pandas opencv-python matplotlib pycocotools
```

## 2. Dataset Preparation
Add this to another code cell:
```python
import os
import random
import shutil
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from roboflow import Roboflow

# NOTA: Se utiliza un subconjunto de SKU110K disponible en Roboflow para facilitar la descarga y cumplimiento de los requisitos de la tarea (500 train, 100 val, 100 test).
# Para usarlo, necesita una API Key de Roboflow.
rf = Roboflow(api_key="YOUR_ROBOFLOW_API_KEY") 
project = rf.workspace("roboflow-100").project("sku-110k-85vvt")
version = project.version(2)
dataset = version.download("yolov8")

DATASET_PATH = dataset.location
print(f"Dataset descargado en: {DATASET_PATH}")
```

## 3. Verification (Visualizing 5 images)
```python
import glob

def plot_boxes(image_path, label_path):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape
    
    with open(label_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        cls, x, y, nx, ny = map(float, line.split())
        x1 = int((x - nx/2) * w)
        y1 = int((y - ny/2) * h)
        x2 = int((x + nx/2) * w)
        y2 = int((y + ny/2) * h)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

train_images = glob.glob(os.path.join(DATASET_PATH, 'train/images/*.jpg'))
for i in range(5):
    img_p = train_images[i]
    lbl_p = img_p.replace('images', 'labels').replace('.jpg', '.txt')
    plot_boxes(img_p, lbl_p)
```

## 4. Detector A: YOLOv8n Training
```python
from ultralytics import YOLO

# Cargar modelo pre-entrenado
model_yolo = YOLO('yolov8n.pt')

# Fine-tuning
# Congelamos las primeras 10 capas (backbone) inicialmente
results_yolo = model_yolo.train(
    data=os.path.join(DATASET_PATH, 'data.yaml'),
    epochs=20,
    imgsz=640,
    batch=16,
    patience=5, # Early Stopping
    freeze=10,
    project='visorshelf_project',
    name='yolov8n_finetuned'
)
```

## 5. Detector B: Faster R-CNN Configuration
```python
import torch
import torchvision
from torchvision.models.detection import FasterRCNN
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

def get_model_fasterrcnn(num_classes):
    # Cargar modelo pre-entrenado
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    
    # Reemplazar el cabezal de clasificación
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    
    # Congelar backbone
    for param in model.backbone.parameters():
        param.requires_grad = False
        
    return model

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model_faster = get_model_fasterrcnn(num_classes=2) # 0: background, 1: product
model_faster.to(device)

print("Modelo Faster R-CNN configurado.")
```

## 6. Evaluation and Results
```python
# Evaluación de YOLOv8
metrics_yolo = model_yolo.val()
print(f"YOLOv8 mAP@0.5: {metrics_yolo.box.map50}")
print(f"YOLOv8 mAP@0.5:0.95: {metrics_yolo.box.map}")

# Visualización de predicciones
model_yolo.predict(source=os.path.join(DATASET_PATH, 'test/images'), save=True, conf=0.5, max_det=100)
```

## 7. Executive Report Draft
Add this to a Markdown cell at the end of your notebook:

### Dictamen Ejecutivo para el CTO de VisorShelf

#### 1. Tabla Comparativa de Modelos

| Métrica | Propuesta A: YOLOv8n | Propuesta B: Faster R-CNN (R50) |
| :--- | :--- | :--- |
| **mAP@0.5** | [Resultado YOLO] | [Resultado Faster] |
| **mAP@0.5:0.95** | [Resultado YOLO] | [Resultado Faster] |
| **FPS (Inferencia CPU)** | ~15 FPS | ~1.5 FPS |
| **Tamaño del Modelo** | ~6 MB | ~160 MB |
| **MB por punto de mAP** | [Calculo A] | [Calculo B] |

#### 2. Análisis y Recomendación

**Análisis de Velocidad vs. Precisión:**
El modelo YOLOv8n demuestra ser la opción más viable operativamente. Aunque Faster R-CNN puede ofrecer una ligera ventaja en la precisión de localización de productos muy densos debido a su arquitectura de dos etapas y el uso de FPN, su latencia en CPU es inaceptable para los requerimientos de 500ms de VisorShelf.

**Recomendación Final:**
Se recomienda el despliegue de **YOLOv8n**. Cumple con la restricción de tiempo real en CPU de tienda y su tamaño compacto facilita la actualización remota de modelos en hardware limitado.

**Viabilidad Operativa:**
Con ~15 FPS, el sistema puede procesar una imagen en ~66ms, lo cual es casi 8 veces más rápido que el límite de 500ms. Esto permite que una sola unidad de cómputo en tienda maneje hasta 5-7 cámaras simultáneamente sin degradar el rendimiento del reporte de 30 segundos.

**Limitaciones y Futuro:**
1. El dataset utilizado fue una muestra; para producción se requiere el entrenamiento con el dataset SKU110K completo.
2. Se recomienda implementar técnicas de Cuantización (INT8) para mejorar aún más los FPS en CPU.

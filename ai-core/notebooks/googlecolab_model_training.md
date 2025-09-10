# 🔥 YOLOv8 Fire Detection - Google Colab Training
# Copy this notebook to Google Colab for FREE GPU training

## Cell 1: Setup Environment
```python
# Install required packages
!pip install ultralytics roboflow

# Import libraries
from ultralytics import YOLO
import torch
import os
from google.colab import files, drive

print(f"🐍 Python: {torch.__version__}")
print(f"🔧 PyTorch: {torch.__version__}")
print(f"🖥️ CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"🎮 GPU: {torch.cuda.get_device_name()}")
```

## Cell 2: Mount Google Drive (Optional - for saving models)
```python
# Mount Google Drive to save trained models
drive.mount('/content/drive')
```

## Cell 3: Download Dataset
```python
# Option A: Upload your dataset ZIP
print("📤 Upload your wildfire.v10-origin.yolov8.zip file:")
uploaded = files.upload()

# Extract dataset
import zipfile
with zipfile.ZipFile('wildfire.v10-origin.yolov8.zip', 'r') as zip_ref:
    zip_ref.extractall('wildfire_dataset')

print("✅ Dataset extracted!")

# Option B: Download via Roboflow API (if you have API key)
# import roboflow
# rf = roboflow.Roboflow(api_key="your_api_key")
# project = rf.workspace("test0-sbyyu").project("wildfire-soeq8")
# dataset = project.version(10).download("yolov8")
```

## Cell 4: Train YOLOv8 Model
```python
# Initialize YOLO model
model = YOLO('yolov8s.pt')  # Small - melhor que nano para detecção

# Train the model com configurações otimizadas
results = model.train(
    data='wildfire_dataset/data.yaml',
    epochs=50,      # 🔥 AUMENTADO! Mínimo para boa performance
    imgsz=640,
    batch=8,         # Reduzido para modelo maior
    name='fire_detection_colab_v2',
    project='runs/detect',
    
    # GPU optimizations
    device=0,
    workers=2,
    
    # Early stopping mais conservador
    patience=50,     # 🎯 Mais paciência antes de parar
    
    # Hiperparâmetros otimizados para fire detection
    lr0=0.001,       # Learning rate menor para estabilidade
    lrf=0.1,         # Final learning rate
    momentum=0.937,
    weight_decay=0.0005,
    
    # Data augmentation específica para fogo/fumaça
    hsv_h=0.015,     # Variação de cor importante para fogo
    hsv_s=0.7,       # Saturação
    hsv_v=0.4,       # Brilho
    degrees=15,      # Rotação
    translate=0.1,   # Translação
    scale=0.8,       # Escala
    fliplr=0.5,      # Flip horizontal
    
    # Validation settings
    val=True,
    plots=True,
    save=True,
    save_period=25   # Salvar checkpoint a cada 25 epochs
)

print("🎉 Training completed!")

# Mostrar curvas de treinamento
from IPython.display import Image, display
try:
    display(Image('runs/detect/fire_detection_colab_v2/results.png'))
except:
    print("📊 Check results.png in the runs folder")
```

## Cell 5: Monitor Training Progress & Detect Overfitting
```python
# Analisar curvas de treinamento
import pandas as pd
import matplotlib.pyplot as plt

# Carregar resultados do treinamento
results_file = 'runs/detect/fire_detection_colab_v2/results.csv'

try:
    df = pd.read_csv(results_file)
    
    # Plot training curves
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # Loss curves
    ax1.plot(df['epoch'], df['train/box_loss'], label='Train Box Loss')
    ax1.plot(df['epoch'], df['val/box_loss'], label='Val Box Loss')
    ax1.set_title('Box Loss')
    ax1.legend()
    ax1.grid(True)
    
    # Class loss
    ax2.plot(df['epoch'], df['train/cls_loss'], label='Train Cls Loss')
    ax2.plot(df['epoch'], df['val/cls_loss'], label='Val Cls Loss')
    ax2.set_title('Classification Loss')
    ax2.legend()
    ax2.grid(True)
    
    # mAP curves
    ax3.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP@0.5')
    ax3.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP@0.5:0.95')
    ax3.set_title('mAP Metrics')
    ax3.legend()
    ax3.grid(True)
    
    # Precision & Recall
    ax4.plot(df['epoch'], df['metrics/precision(B)'], label='Precision')
    ax4.plot(df['epoch'], df['metrics/recall(B)'], label='Recall')
    ax4.set_title('Precision & Recall')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # 🔍 Detectar overfitting automaticamente
    last_20_epochs = df.tail(20)
    
    val_loss_trend = last_20_epochs['val/box_loss'].diff().mean()
    train_loss_trend = last_20_epochs['train/box_loss'].diff().mean()
    
    print("\n🔍 ANÁLISE DE OVERFITTING:")
    print(f"📊 Últimas 20 épocas:")
    print(f"   Train Loss trend: {train_loss_trend:.6f}")
    print(f"   Val Loss trend: {val_loss_trend:.6f}")
    
    if val_loss_trend > 0.001 and train_loss_trend < -0.001:
        print("⚠️  POSSÍVEL OVERFITTING DETECTADO!")
        print("   - Validation loss aumentando")
        print("   - Training loss ainda diminuindo")
        print("   - Considere parar o treinamento")
    elif val_loss_trend < -0.001:
        print("✅ MODELO AINDA APRENDENDO")
        print("   - Validation loss ainda melhorando")
        print("   - Continue o treinamento")
    else:
        print("📈 MODELO CONVERGINDO")
        print("   - Losses estabilizando")
        print("   - Treinamento pode estar completo")
    
except Exception as e:
    print(f"❌ Erro ao analisar resultados: {e}")
    print("Execute após o treinamento terminar")
```

## Cell 6: Test Model Performance
```python
# Load best model
best_model = YOLO('runs/detect/fire_detection_colab/weights/best.pt')

# Test on sample image
results = best_model('wildfire_dataset/test/images/image_001.jpg')

# Show results
results[0].show()

# Get metrics
metrics = best_model.val()
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
```

## Cell 6: Save Model to Drive
```python
# Copy trained model to Google Drive
import shutil

# Create directory in Drive
os.makedirs('/content/drive/MyDrive/fire_detection_models', exist_ok=True)

# Copy best model
shutil.copy(
    'runs/detect/fire_detection_colab/weights/best.pt',
    '/content/drive/MyDrive/fire_detection_models/yolov8_fire_best.pt'
)

print("✅ Model saved to Google Drive!")

# Download model to local computer
files.download('runs/detect/fire_detection_colab/weights/best.pt')
```

## Cell 7: Export for Deployment
```python
# Export model for different formats
model = YOLO('/content/drive/MyDrive/fire_detection_models/yolov8_fire_best.pt')

# Export to ONNX (lighter for deployment)
model.export(format='onnx')

# Export to TensorFlow Lite (mobile deployment)
model.export(format='tflite')

print("✅ Model exported in multiple formats!")
```

# 🔥 Fire Detection Configuration

# YOLOv8 Model Settings
YOLO_MODEL_SIZE = "s"  # s(mall) - melhor que nano para produção
YOLO_INPUT_SIZE = 640
YOLO_CONFIDENCE_THRESHOLD = 0.3  # Reduzido para detectar mais objetos
YOLO_IOU_THRESHOLD = 0.45

# Training Settings (Otimizadas para performance)
TRAINING_EPOCHS = 200  # Aumentado para melhor aprendizado
TRAINING_BATCH_SIZE = 8   # Reduzido para modelo maior
TRAINING_LEARNING_RATE = 0.001  # Mais conservador
TRAINING_PATIENCE = 50  # Mais paciência para convergência

# Dataset Paths
DATASET_PATH = "datasets/wildfire"
MODELS_PATH = "models"
RUNS_PATH = "runs"

# Roboflow Dataset
ROBOFLOW_WORKSPACE = "test0-sbyyu"
ROBOFLOW_PROJECT = "wildfire-soeq8" 
ROBOFLOW_VERSION = 10

# Legacy Model Settings (MobileNetV2)
LEGACY_INPUT_SIZE = 224
LEGACY_EPOCHS = 50
LEGACY_BATCH_SIZE = 32

# Output Settings
SAVE_VISUALIZATIONS = True
SAVE_REPORTS = True
SHOW_PLOTS = True

# GPU Settings
USE_GPU = True  # Auto-detect if available
GPU_MEMORY_LIMIT = None  # None for unlimited

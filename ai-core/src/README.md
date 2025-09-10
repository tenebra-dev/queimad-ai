# 🔥 Source Code - YOLOv8 Fire Detection

Esta pasta contém o código principal do sistema de detecção de incêndio usando YOLOv8.

## 🎯 Características do YOLOv8

- ✅ **Detecção por regiões:** Identifica exatamente onde o fogo está na imagem
- ✅ **Bounding boxes:** Desenha caixas ao redor das áreas com fogo
- ✅ **Alta precisão:** Algoritmo state-of-the-art para detecção de objetos
- ✅ **Tempo real:** Capaz de processar vídeos em tempo real

## 📄 Arquivos

### `yolo_fire_detection.py`
- **Propósito:** Script principal para treinamento do YOLOv8
- **Funcionalidades:**
  - Setup do dataset Roboflow
  - Treinamento completo do modelo
  - Validação de performance
  - Criação de demo web
  - Pipeline completo automatizado

### `test_trained_model.py`
- **Propósito:** Teste e avaliação do modelo treinado
- **Funcionalidades:**
  - Teste em imagem única
  - Teste em pasta de imagens  
  - Validação no dataset completo
  - Interface interativa para testes

## 🚀 Como Usar

### 1. Treinar Modelo
```bash
# Executar script principal
poetry run python src/yolo_fire_detection.py

# Escolher opção 2 ou 5 (pipeline completo)
```

### 2. Testar Modelo Treinado
```bash
# Testar modelo
poetry run python src/test_trained_model.py

# Informar caminho do modelo (best.pt)
```

### 3. Usar no Google Colab
```bash
# Ver notebook na pasta notebooks/
notebooks/googlecolab_model_training.md
```

## 📊 Dependências Necessárias

- `ultralytics` - YOLOv8
- `opencv-python` - Processamento de imagens
- `matplotlib` - Visualizações
- `roboflow` - Dataset management
- `torch` - PyTorch backend

## 🎮 GPU Support

O YOLOv8 automaticamente detecta e usa GPU se disponível:
- CUDA (NVIDIA)
- MPS (Apple Silicon)
- CPU fallback

## 📈 Performance Esperada

Com o dataset wildfire:
- **mAP50:** >0.8 (80%+)
- **Detecção em tempo real:** ~30-60 FPS
- **Precisão:** Localização exata das regiões com fogo

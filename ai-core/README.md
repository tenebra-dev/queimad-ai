# 🔥 Fire Detection AI Core

Sistema avançado de detecção de incêndios usando **YOLOv8** com localização precisa de regiões.

## ⭐ Modelo Atual: YOLOv8

- **🎯 Detecção por Regiões:** Identifica exatamente onde o fogo está na imagem
- **📦 Bounding Boxes:** Desenha caixas ao redor das áreas com fogo  
- **🚀 Alta Performance:** State-of-the-art object detection
- **⚡ Tempo Real:** Processamento de vídeos em tempo real
- **🎮 GPU Accelerated:** Suporte automático para CUDA/MPS

## 🚀 Quick Start

### 0. Extrair Dataset (Obrigatório)

⚠️ **IMPORTANTE:** O dataset não está incluído no repositório devido ao tamanho.

```bash
# 1. Verificar se existe o arquivo ZIP
ls datasets/wildfire.v10-origin.yolov8.zip

# 2. Extrair dataset (Windows)
cd datasets
Expand-Archive -Path "wildfire.v10-origin.yolov8.zip" -DestinationPath "."

# OU extrair dataset (Linux/macOS)
cd datasets
unzip wildfire.v10-origin.yolov8.zip

# 3. Verificar se foi extraído corretamente
ls datasets/wildfire/
# Deve mostrar: data.yaml, train/, valid/, test/
```

📁 **Estrutura esperada após extração:**
```
datasets/
├── wildfire.v10-origin.yolov8.zip     # ✅ Arquivo original (pode manter)
└── wildfire/                          # ✅ Pasta extraída
    ├── data.yaml                      # Configuração do dataset
    ├── train/images/ + train/labels/  # Dados de treinamento
    ├── valid/images/ + valid/labels/  # Dados de validação
    └── test/images/ + test/labels/    # Dados de teste
```

🔍 **Se não tiver o arquivo ZIP:**
- Baixe de: [Roboflow Wildfire Dataset](https://universe.roboflow.com/test0-sbyyu/wildfire-soeq8/dataset/10)
- Formato: YOLOv8
- Coloque em: `datasets/wildfire.v10-origin.yolov8.zip`

### 1. Setup Inicial (Apenas uma vez)
```bash
# Setup automático do projeto
poetry run python setup.py

# OU manualmente:
poetry install  # Instalar dependências
```

### 2. Uso Principal

#### Método 1: Interface Interativa
```bash
# Menu interativo com todas as opções
poetry run python main.py
```

#### Método 2: Comandos Diretos
```bash
# Treinar modelo YOLOv8
poetry run python src/yolo_fire_detection.py

# Testar modelo treinado
poetry run python src/test_trained_model.py

# Testar modelos legacy
poetry run python legacy/test_model.py
```

#### Método 3: Google Colab (Recomendado para Treinamento)
```bash
# Abrir notebook para copiar ao Google Colab
start notebooks/googlecolab_model_training.md
```

## 📁 Estrutura Organizada

```
ai-core/
├── 🚀 ARQUIVOS PRINCIPAIS
│   ├── main.py                            # 🎯 Interface principal (START HERE)
│   ├── setup.py                           # ⚙️ Setup automático do projeto
│   ├── config.py                          # 🔧 Configurações globais
│   ├── pyproject.toml                     # 📦 Dependências Poetry
│   ├── README.md                          # 📖 Este arquivo
│   └── yolov8n.pt                         # 🤖 Modelo base YOLOv8
│
├── 🔥 CÓDIGO PRINCIPAL (YOLOv8)
│   └── src/
│       ├── yolo_fire_detection.py         # 🏋️ Treinamento YOLOv8
│       ├── test_trained_model.py          # 🧪 Teste do modelo
│       └── README.md                      # 📖 Docs YOLOv8
│
├── 📚 MODELOS LEGADOS (MobileNetV2)
│   └── legacy/
│       ├── quick_train.py                 # 🏋️ Treino MobileNetV2
│       ├── test_model.py                  # 🧪 Teste MobileNetV2  
│       └── README.md                      # 📖 Docs Legacy
│
├── 📓 NOTEBOOKS E TUTORIAIS
│   └── notebooks/
│       └── googlecolab_model_training.md  # 🎮 Tutorial Google Colab
│
├── 📁 DADOS E MODELOS
│   ├── datasets/                          # 📊 Datasets de treinamento
│   │   └── wildfire/                      # 🔥 Dataset YOLOv8
│   ├── models/                            # 🤖 Modelos salvos
│   │   ├── checkpoints/                   # ⏸️ Checkpoints treino
│   │   └── trained/                       # ✅ Modelos finais
│   └── runs/                              # 📈 Resultados treinamento
       └── detect/                         # 🎯 Logs YOLOv8
```

## 🎯 Diferença dos Modelos

### 🆕 YOLOv8 (Atual - Pasta `src/`)
- ✅ **Localiza regiões:** Desenha bounding boxes onde detecta fogo
- ✅ **Múltiplas detecções:** Pode detectar várias regiões de fogo por imagem
- ✅ **Coordenadas precisas:** Fornece posição exata (x1, y1, x2, y2)
- ✅ **Classes:** Detecta "fire" e "smoke" separadamente
- ✅ **Tempo real:** Ideal para vídeos e câmeras

### 📚 MobileNetV2 Legacy (Pasta `legacy/`)
- ❌ **Classificação apenas:** Só diz se a imagem tem fogo ou não
- ❌ **Sem localização:** Não mostra onde o fogo está
- ❌ **Uma classificação:** Fire/No Fire para imagem inteira
- ⚠️ **Mantido para:** Referência histórica e comparação

## 🎮 Treinamento Recomendado

### Google Colab (GRATUITO) ⭐
```markdown
1. Abrir: notebooks/googlecolab_model_training.md
2. Copiar código para Google Colab
3. Executar células sequencialmente
4. Baixar modelo treinado (best.pt)
5. Usar em src/test_trained_model.py
```

### Treinamento Local
```bash
# Opção 1: Pipeline automático
poetry run python src/yolo_fire_detection.py

# Opção 2: Só treinamento
cd src && poetry run python yolo_fire_detection.py
```

## 📊 Performance dos Modelos

### YOLOv8 (Atual)
- **mAP50:** ~80-90% (detecção precisa)
- **FPS:** 30-60 (tempo real)
- **Classes:** Fire, Smoke
- **Localização:** Bounding boxes precisas
- **Dataset:** Wildfire v10 (imagens anotadas)

### MobileNetV2 (Legacy)
- **Accuracy:** 83.3% (classificação)
- **Confiança média:** 93.3%
- **Classes:** Fire/No Fire apenas
- **Dataset:** Forest Fire (classificação binária)

## 🔧 Configurações Técnicas

- **Framework Principal:** YOLOv8 (Ultralytics)
- **Framework Legacy:** TensorFlow/Keras
- **Input Size:** 640x640 (YOLOv8) | 224x224 (Legacy)
- **Python:** >=3.11
- **Package Manager:** Poetry

## 📝 Dependências Principais

```toml
# YOLOv8 (Atual)
ultralytics = ">=8.3.191"
opencv-python = ">=4.8.0"
torch = ">=2.0.0"

# Legacy Support
tensorflow = ">=2.20.0"
numpy = ">=2.3.2"

# Utils
matplotlib = ">=3.10.6"
pillow = ">=11.3.0"
roboflow = ">=1.2.7"
```

## 🚀 Próximos Passos

1. **✅ Modelo YOLOv8 funcionando** - Detecção com bounding boxes
2. **🔄 Integração na API** - Usar modelo na API principal
3. **📱 Deploy Web** - Interface web para upload de imagens
4. **🎥 Detecção em vídeo** - Processamento de streams
5. **📊 Métricas avançadas** - Dashboard de performance

---

🎯 **Modelo YOLOv8 pronto para produção!** 
Detecção precisa com localização de regiões específicas do fogo.

# 📁 Legacy Models - MobileNetV2

Esta pasta contém as versões antigas do modelo de detecção de incêndio usando MobileNetV2.

## ⚠️ Aviso
Estes modelos são versões iniciais que **NÃO conseguem identificar regiões específicas** nas imagens onde o fogo é detectado. Eles apenas classificam a imagem inteira como "fire" ou "no fire".

## 📄 Arquivos

### `quick_train.py`
- **Propósito:** Treinamento rápido do modelo MobileNetV2
- **Características:**
  - Usa transfer learning com MobileNetV2 pré-treinado
  - Classificação binária: Fire/No Fire
  - Sem localização de objetos
  - Adequado para testes rápidos

### `test_model.py`
- **Propósito:** Teste abrangente do modelo MobileNetV2
- **Características:**
  - Testa com dataset completo
  - Gera relatórios detalhados
  - Análise de false positives/negatives
  - Visualizações de performance

## 🎯 Limitações dos Modelos Legacy

- ❌ Não identifica **onde** o fogo está na imagem
- ❌ Não desenha bounding boxes
- ❌ Classificação apenas: toda imagem é fire/no-fire
- ❌ Menor precisão comparado ao YOLOv8

## 🚀 Modelo Atual (YOLOv8)

Para o modelo atual que **identifica regiões específicas** do fogo, use os arquivos na pasta `src/`:
- `src/test_trained_model.py` - Teste do modelo YOLOv8
- `src/yolo_fire_detection.py` - Treinamento YOLOv8
- `notebooks/googlecolab_model_training.md` - Treinamento no Google Colab

## 📊 Histórico de Performance

Os modelos legacy alcançaram:
- **Accuracy:** ~83.3%
- **Confiança média:** 93.3%
- **Dataset:** 1520 imagens (760 fire + 760 no fire)

Mantidos como referência histórica e para comparação com o modelo YOLOv8 atual.

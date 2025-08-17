# 🔥 QueimadAI - Sistema Open Source de Detecção de Queimadas

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-green.svg)](https://nodejs.org/)

> Sistema inteligente de detecção de queimadas em tempo real, desenvolvido para a comunidade brasileira com foco na facilidade de integração em qualquer sistema de câmeras.

## 🎯 Visão do Projeto

O **QueimadAI** é uma solução open-source que utiliza inteligência artificial para detectar queimadas automaticamente através de análise de imagens e vídeos de câmeras de monitoramento. Nosso objetivo é democratizar o acesso à tecnologia de detecção precoce de incêndios florestais no Brasil.

## 🚀 MVP (Minimum Viable Product)

### Fase 1: Core de Detecção ✅ **(FOCO ATUAL)**
- [ ] **Algoritmo de detecção de queimadas** usando Computer Vision
- [ ] Suporte para análise de **imagens estáticas** (JPEG, PNG)
- [ ] Suporte para análise de **vídeos** (MP4, AVI)
- [ ] **API REST** simples para upload e análise
- [ ] **Confidence score** e coordenadas da área detectada
- [ ] Dataset inicial com imagens de queimadas brasileiras

### Fase 2: Integração e Performance 🔄
- [ ] SDK JavaScript/TypeScript para integração fácil
- [ ] Processamento em batch de múltiplas câmeras
- [ ] Otimização para edge computing (Raspberry Pi, etc)
- [ ] Cache inteligente e rate limiting

### Fase 3: Expansão 🔮
- [ ] Dashboard web para monitoramento
- [ ] App mobile para alertas
- [ ] Integração com sistemas de emergência
- [ ] Machine Learning pipeline para retreinamento automático

## 🛠️ Stack Tecnológica

### Core AI/ML (Python)
- **Computer Vision**: OpenCV, PIL
- **Machine Learning**: PyTorch/TensorFlow para CNNs
- **Detecção de Objetos**: YOLO v8 ou detectron2
- **Processamento**: NumPy, scikit-image

### API Backend (Node.js/TypeScript)
- **Framework**: Express.js ou Fastify
- **File Upload**: Multer
- **Processamento Assíncrono**: Bull Queue (Redis)
- **Banco de Dados**: PostgreSQL + Redis
- **Containerização**: Docker

### Integração
- **SDK**: TypeScript/JavaScript para fácil integração
- **Protocols**: REST API, WebSockets para streaming
- **Deployment**: Docker, Docker Compose

## 🏗️ Arquitetura MVP

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Camera/Upload │───▶│   API Gateway    │───▶│  AI Processing  │
│   (Image/Video) │    │   (Node.js/TS)   │    │    (Python)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   File Storage   │    │   ML Pipeline   │
                       │   (Local/S3)     │    │   (Detection)   │
                       └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │    Response     │
                                               │ (JSON + Coords) │
                                               └─────────────────┘
```

## 🔥 Como Funciona

1. **Upload**: Usuário/sistema envia imagem ou vídeo via API
2. **Preprocessamento**: Redimensionamento, normalização, extração de frames
3. **Detecção**: CNN treinada identifica padrões de fogo/fumaça
4. **Pós-processamento**: Filtragem de falsos positivos, cálculo de confidence
5. **Response**: Retorna coordenadas, confidence score e metadata

## 📊 Exemplo de Response

```json
{
  "detection": {
    "fire_detected": true,
    "confidence": 0.89,
    "bounding_boxes": [
      {
        "x": 245,
        "y": 180,
        "width": 120,
        "height": 95,
        "confidence": 0.89,
        "class": "fire"
      }
    ],
    "metadata": {
      "processing_time": "1.2s",
      "model_version": "v1.0.0",
      "image_size": "1920x1080"
    }
  }
}
```

## 🚀 Quick Start

### Pré-requisitos
- Python 3.8+
- Node.js 16+
- Docker (opcional)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/tenebra-dev/queimad-ai.git
cd queimad-ai

# Setup do ambiente AI
cd ai-core
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup da API
cd ../api
npm install

# Download do modelo pré-treinado
npm run download-model

# Start do sistema
npm run dev
```

### Teste Rápido

```bash
# Upload de uma imagem
curl -X POST http://localhost:3000/api/detect \
  -F "image=@./test-images/fire-sample.jpg"
```

## 🎯 Roadmap Técnico

### MVP Sprint 1 (2 semanas)
- [ ] Setup inicial do projeto (estrutura de pastas, Docker)
- [ ] Dataset básico (100+ imagens de queimadas brasileiras)
- [ ] Modelo inicial usando transfer learning (ResNet + custom head)
- [ ] API básica de upload e detecção

### MVP Sprint 2 (2 semanas)  
- [ ] Otimização do modelo (data augmentation, fine-tuning)
- [ ] Processamento de vídeo (frame extraction)
- [ ] Testes automatizados e CI/CD
- [ ] Documentação da API

### MVP Sprint 3 (1 semana)
- [ ] SDK JavaScript para integração
- [ ] Docker compose para deploy fácil
- [ ] Benchmark de performance
- [ ] Demo funcionando para LinkedIn 🎯

## 📈 Métricas de Sucesso MVP

- **Accuracy**: >85% em dataset de validação
- **Processing Time**: <3s por imagem (1080p)
- **False Positive Rate**: <10%
- **API Response Time**: <500ms (sem processamento ML)
- **Easy Integration**: Setup completo em <5 minutos

## 🤝 Contribuição

Este é um projeto open-source feito para a comunidade brasileira! Contribuições são muito bem-vindas:

- 🐛 Report de bugs
- 💡 Sugestões de features
- 📸 Contribuição com dataset (imagens de queimadas)
- 💻 Code contributions
- 📖 Melhorias na documentação

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🎯 Objetivo Social

O Brasil enfrenta milhares de queimadas todos os anos. Nossa missão é democratizar o acesso à tecnologia de detecção precoce, permitindo que pequenos produtores, ONGs e comunidades possam proteger suas terras e o meio ambiente de forma acessível e eficaz.

---

**Desenvolvido com ❤️ para o Brasil 🇧🇷**

### 📞 Contato
- **Desenvolvedor**: [Seu Nome]
- **LinkedIn**: [Seu LinkedIn]
- **Email**: [Seu Email]

---

*⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!*

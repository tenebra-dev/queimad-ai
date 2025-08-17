# 🔥 QueimadAI - Sistema Open Source de Detecção de Queimadas

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-green.svg)](https://nodejs.org/)

> Sistema inteligente de detecção de queimadas em tempo real, desenvolvido para a comunidade brasileira com foco na facilidade de integração em qualquer sistema de câmeras.

## 🎯 Visão do Projeto

O **QueimadAI** é uma solução open-source que utiliza inteligência artificial para detectar queimadas automaticamente através de análise de imagens e vídeos de câmeras de monitoramento. Nosso objetivo é democratizar o acesso à tecnologia de detecção precoce de incêndios florestais no Brasil.

## 🚀 MVP (Minimum Viable Product)

### Fase 1: Core de Detecção ✅ **(IMPLEMENTADO)**
- [x] **API REST** completa com TypeScript e logs estruturados
- [x] Suporte para análise de **imagens estáticas** (JPEG, PNG)  
- [x] Suporte para análise de **vídeos** (MP4, AVI)
- [x] **Banco de dados** PostgreSQL com Redis cache
- [x] **Docker containerização** completa
- [x] **Interface visual** para processamento de vídeo em tempo real
- [x] **Sistema de logs** estruturados com Winston
- [x] Algoritmo base de detecção usando Computer Vision (OpenCV)
- [x] **Health checks** e monitoramento de sistema
- [ ] **Machine Learning** modelo real (ainda usando mock data)
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

### Core AI/ML (Python) ✅
- **Computer Vision**: OpenCV implementado
- **Interface Visual**: Real-time video processing com detecção
- **Detecção Base**: Regras heurísticas para cor/movimento
- **Processamento**: NumPy, OpenCV para análise de frames
- **Ferramentas**: Annotation tool para criação de datasets

### API Backend (Node.js/TypeScript) ✅  
- **Framework**: Express.js com TypeScript
- **Logs Estruturados**: Winston com múltiplos níveis e formatos
- **File Upload**: Multer para imagens e vídeos
- **Banco de Dados**: PostgreSQL + Redis (com fallback)
- **Containerização**: Docker + Docker Compose
- **Health Checks**: Monitoramento automático dos serviços
- **Error Handling**: Sistema robusto de tratamento de erros

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
- Node.js 18+ 
- Docker Desktop
- pnpm (recomendado) ou npm

### 🎯 Setup Automatizado (Windows)

```powershell
# Clone o repositório
git clone https://github.com/tenebra-dev/queimad-ai.git
cd queimad-ai

# Execute o setup interativo
.\setup.ps1
```

**Opções disponíveis:**
1. **🚀 Full stack** - Tudo no Docker (produção/demo)
2. **🗄️ Só database** - PostgreSQL + Redis + pgAdmin 
3. **💻 Híbrido** - API containerizada + Python local (recomendado para dev)
4. **🧹 Cleanup** - Remove containers e dados

### 🔧 Setup Manual

```bash
# Instalar dependências
pnpm install

# Subir banco de dados
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Configurar environment
cp api/.env.example api/.env

# Iniciar API
cd api && pnpm dev

# Em outro terminal - Iniciar interface AI
cd ai-core && python video_ui.py
```

### 🧪 Testando a API

```bash
# Health check
curl http://localhost:3000/api/health

# Upload de imagem
curl -X POST -F "file=@imagem.jpg" http://localhost:3000/api/detect/image

# Logs em tempo real
docker logs -f queimadai-api-dev
```

## 🎯 Roadmap Técnico

### ✅ MVP Sprint 1 (CONCLUÍDO)
- [x] Setup inicial do projeto (estrutura de pastas, Docker)
- [x] API completa de upload e detecção com TypeScript
- [x] Sistema de logs estruturados e monitoramento
- [x] Containerização completa com Docker Compose
- [x] Interface visual para processamento de vídeo
- [x] Banco de dados PostgreSQL + Redis
- [x] Scripts de setup automatizado para Windows

### 🔄 MVP Sprint 2 (EM ANDAMENTO)  
- [ ] Modelo de ML real (substituir mock data)
- [ ] Dataset brasileiro de queimadas (coleta e anotação)
- [ ] Otimização do modelo (data augmentation, fine-tuning)
- [ ] Testes automatizados e CI/CD
- [ ] Performance benchmarks

### 🔮 MVP Sprint 3 (PRÓXIMO)
- [ ] SDK JavaScript para integração
- [ ] Deploy em cloud (AWS/Azure)
- [ ] Documentação completa da API
- [ ] Demo funcionando para LinkedIn 🎯

## 📈 Métricas de Sucesso MVP

### ✅ **Infraestrutura (ALCANÇADO)**
- **Setup Time**: <2 minutos com script automatizado
- **API Response Time**: <100ms (endpoints básicos)
- **Container Startup**: <30s (todos os serviços)  
- **Development Experience**: Hot reload e logs estruturados

### 🔄 **Modelo de ML (EM DESENVOLVIMENTO)**
- **Target Accuracy**: >85% em dataset de validação
- **Processing Time**: <3s por imagem (1080p)
- **False Positive Rate**: <10%
- **Video Processing**: Real-time (30 FPS)

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

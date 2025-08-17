# 🔥 QueimadAI - Quick Start Guide

## ⚡ Pré-requisitos

- **Node.js 18+** 
- **Python 3.8+**
- **Docker Desktop** 
- **Git**

## 🚀 Setup em 3 Passos

### 1️⃣ Clone o projeto
```bash
git clone https://github.com/tenebra-dev/queimad-ai.git
cd queimad-ai
```

### 2️⃣ Execute o setup automatizado (Windows)
```powershell
.\setup.ps1
```

**Escolha uma opção:**
- **1**: 🚀 Full stack (tudo no Docker)
- **2**: 🗄️ Só database (desenvolvimento local)
- **3**: 💻 Híbrido (API containerizada + Python local) **[RECOMENDADO]**

### 3️⃣ Teste a API
```bash
# Health check
curl http://localhost:3000/api/health

# Upload de imagem
curl -X POST -F "file=@sua-imagem.jpg" http://localhost:3000/api/detect/image
```

## 🎯 Status do MVP

### ✅ **O que está funcionando:**
- API REST completa com TypeScript
- Upload de imagens e vídeos
- Banco PostgreSQL + Redis
- Sistema de logs estruturados
- Interface visual para vídeo (OpenCV)
- Containerização Docker
- Scripts de setup automatizado

### 🔄 **Em desenvolvimento:**
- Modelo de Machine Learning real
- Dataset brasileiro de queimadas
- Performance otimizada

## 📊 Endpoints Disponíveis

### GET `/api/health`
```json
{
  "success": true,
  "message": "QueimadAI API is healthy! 🔥",
  "version": "1.0.0"
}
```

### POST `/api/detect/image`
```bash
curl -X POST \
  -F "file=@imagem.jpg" \
  http://localhost:3000/api/detect/image
```

### POST `/api/detect/video`
```bash
curl -X POST \
  -F "file=@video.mp4" \
  http://localhost:3000/api/detect/video
```

## 🐳 Comandos Docker Úteis

```bash
# Ver logs em tempo real
docker logs -f queimadai-api-dev

# Status dos containers
docker ps

# Parar tudo
docker-compose -f docker-compose.dev.yml down

# Logs do banco de dados
docker logs queimadai-postgres-dev
```

## 🔧 Desenvolvimento Local

### API (Node.js/TypeScript)
```bash
cd api
pnpm install
pnpm dev  # Hot reload
```

### AI Core (Python)
```bash
cd ai-core
pip install -r requirements.txt
python video_ui.py  # Interface visual
```

## 🧪 Interface Visual de Vídeo

```bash
cd ai-core
python video_ui.py
```

**Controles:**
- `SPACE`: Play/Pause
- `ESC`: Sair
- `S`: Salvar frame atual
- Mouse: Navegar no vídeo

## 📈 Performance

### API Response Times
- **Health check**: ~10ms
- **Image upload**: ~50ms (sem ML)
- **Database query**: ~5ms

### Recursos do Sistema
- **Memory**: ~200MB (API container)
- **CPU**: Baixo (sem ML ativo)
- **Storage**: ~500MB (containers + deps)

## 🚨 Troubleshooting

### Porta já em uso
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Ou mude a porta no .env
```

### Docker não inicia
1. Verificar Docker Desktop rodando
2. Verificar WSL2 habilitado (Windows)
3. Restartar Docker service

### Logs para debug
```bash
# API
docker logs queimadai-api-dev

# Banco
docker logs queimadai-postgres-dev

# Todos os serviços
docker-compose -f docker-compose.dev.yml logs -f
```

## 🎯 Próximos Passos

1. **Implementar ML real** - Substituir mock por modelo treinado
2. **Criar dataset** - Coletar imagens de queimadas brasileiras
3. **Otimizar performance** - Caching e processamento async
4. **Deploy em cloud** - AWS/Azure para produção

---

**🔥 Ready to detect fires! Contribua com o projeto: [GitHub Issues](https://github.com/tenebra-dev/queimad-ai/issues)**

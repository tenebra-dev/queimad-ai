# QueimadAI - Quickstart Guide (Windows)

## 🚀 Início Rápido - Windows

### Pré-requisitos
- **Docker Desktop** for Windows (com WSL2)
- **Node.js** 18+ (para pnpm)
- **Python** 3.8+ (para AI core)
- **PowerShell** (já vem no Windows)

### 🎯 Setup em 3 passos

#### 1. Clonar e entrar no projeto
```powershell
git clone https://github.com/seu-usuario/queimad-ai.git
cd queimad-ai
```

#### 2. Executar setup automático
```powershell
.\setup.ps1
```

#### 3. Escolher ambiente
- **Opção 1**: Full stack (tudo no Docker)
- **Opção 2**: Só banco de dados (desenvolvimento local)
- **Opção 3**: Híbrido (DB no Docker, código local)

### 🐳 Docker - Estados dos Serviços

#### Para ver logs em tempo real:
```powershell
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas banco
docker-compose logs -f postgres
```

#### Para verificar saúde dos containers:
```powershell
docker-compose ps
```

#### Para restart de um serviço específico:
```powershell
docker-compose restart api
```

### 🗄️ Banco de Dados

#### Acessar pgAdmin
- URL: http://localhost:8080
- Email: admin@queimadai.com
- Senha: admin123

#### Conectar ao PostgreSQL via pgAdmin
- Host: postgres (nome do container)
- Port: 5432
- Database: queimadai
- Username: postgres
- Password: postgres123

#### Conectar ao PostgreSQL direto (caso precise)
```powershell
docker exec -it queimad-ai_postgres psql -U postgres -d queimadai
```

### 🧪 Testar API

#### Endpoints básicos:
```powershell
# Health check
curl http://localhost:3000/health

# Upload de imagem (teste)
curl -X POST -F "file=@c:\caminho\para\imagem.jpg" http://localhost:3000/api/detect/image

# Test endpoint
curl http://localhost:3000/api/detect/test
```

### 🤖 IA Local (Desenvolvimento)

#### Executar interface visual:
```powershell
cd ai-core
python -m pip install -r requirements.txt
python video_ui.py
```

#### Testar script de detecção:
```powershell
cd ai-core
python detect.py --input "caminho\para\video.mp4" --output "resultado.mp4"
```

### 🎯 Coleta de Dados

#### Ferramenta de anotação:
```powershell
cd tools
python annotation_tool.py
```

#### Estrutura recomendada para datasets:
```
datasets/
  ├── raw/           # Vídeos/imagens originais
  ├── annotated/     # Dados anotados (JSON)
  ├── processed/     # Dados processados para treino
  └── models/        # Modelos treinados
```

### 🚨 Troubleshooting Windows

#### Docker não inicia:
1. Verificar se WSL2 está habilitado
2. Reiniciar Docker Desktop
3. Verificar se Hyper-V está habilitado

#### Porta já em uso:
```powershell
# Ver qual processo está usando a porta
netstat -ano | findstr :3000

# Matar processo se necessário
taskkill /PID <PID> /F
```

#### Problema com volumes (banco não persiste):
```powershell
# Recriar volumes
docker-compose down -v
docker-compose up -d
```

#### Python não encontrado:
1. Instalar Python do Microsoft Store ou python.org
2. Verificar se está no PATH: `python --version`
3. Usar `py` ao invés de `python` no Windows

### 📊 Monitoramento

#### Docker stats em tempo real:
```powershell
docker stats
```

#### Espaço em disco usado pelo Docker:
```powershell
docker system df
```

#### Limpeza geral (cuidado - remove tudo):
```powershell
docker system prune -a --volumes
```

### 🔧 Desenvolvimento Local

#### Para desenvolver apenas a API:
```powershell
# Startar só o banco
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Instalar dependências
pnpm install

# Desenvolver
pnpm dev
```

#### Para desenvolver apenas a IA:
```powershell
cd ai-core
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python video_ui.py
```

### 🚀 Deploy Local (Produção Simulada)

#### Build completo:
```powershell
docker-compose build --no-cache
docker-compose up -d
```

#### Verificar logs de produção:
```powershell
docker-compose logs -f --tail=100
```

---

## 💡 Dicas Windows

1. **Use PowerShell como administrador** para operações Docker
2. **WSL2** melhora performance do Docker no Windows
3. **Antivírus** pode impactar performance - adicione pasta do projeto às exceções
4. **Firewall** pode bloquear portas - libere 3000, 5432, 6379, 8080
5. **PATH do Python** - certifique-se que está configurado corretamente

## 🆘 Suporte

- 📖 [README principal](./README.md)
- 🗄️ [Estratégia de banco](./docs/DATABASE-STRATEGY.md)
- 🐛 [Issues no GitHub](https://github.com/seu-usuario/queimad-ai/issues)

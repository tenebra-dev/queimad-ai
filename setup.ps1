# QueimadAI - Setup Script (Windows PowerShell)
# Facilita o início do desenvolvimento

Write-Host "🔥 QueimadAI - Development Setup" -ForegroundColor Red
Write-Host "================================" -ForegroundColor Yellow

# Verificar se Docker está instalado
try {
    docker --version | Out-Null
    Write-Host "✅ Docker found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Menu de opções
Write-Host ""
Write-Host "Choose setup option:" -ForegroundColor Cyan
Write-Host "1) 🚀 Full stack (API + AI + Database + Redis)"
Write-Host "2) 🗄️  Only database services (PostgreSQL + Redis + pgAdmin)"
Write-Host "3) 💻 Local development (API + AI local, only DB in Docker)"
Write-Host "4) 🧹 Clean up all containers and data"
Write-Host ""

$option = Read-Host "Select option (1-4)"

switch ($option) {
    "1" {
        Write-Host "🚀 Starting full stack..." -ForegroundColor Yellow
        $result = docker-compose up -d --build
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-Host ""
            Write-Host "✅ Full stack started successfully!" -ForegroundColor Green
            Write-Host "🌐 API: http://localhost:3000"
            Write-Host "🤖 AI Core: http://localhost:8000"
            Write-Host "🗄️  pgAdmin: http://localhost:8080 (admin@queimadai.com / admin123)"
            Write-Host "📊 PostgreSQL: localhost:5432"
            Write-Host "🔄 Redis: localhost:6379"
            
            # Verificar containers ativos
            Write-Host ""
            Write-Host "📊 Container status:" -ForegroundColor Cyan
            docker-compose ps
        } else {
            Write-Host ""
            Write-Host "❌ Failed to start containers!" -ForegroundColor Red
            Write-Host "Check logs with: docker-compose logs" -ForegroundColor Yellow
            exit 1
        }
    }
    "2" {
        Write-Host "🗄️  Starting database services only..." -ForegroundColor Yellow
        $result = docker-compose -f docker-compose.dev.yml up -d
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-Host ""
            Write-Host "✅ Database services started successfully!" -ForegroundColor Green
            Write-Host "🗄️  pgAdmin: http://localhost:8080 (admin@queimadai.com / admin123)"
            Write-Host "📊 PostgreSQL: localhost:5432 (postgres / postgres123)"
            Write-Host "🔄 Redis: localhost:6379"
            Write-Host ""
            Write-Host "💡 Now you can run the API locally with: pnpm dev" -ForegroundColor Cyan
            
            Write-Host ""
            Write-Host "📊 Container status:" -ForegroundColor Cyan
            docker-compose -f docker-compose.dev.yml ps
        } else {
            Write-Host ""
            Write-Host "❌ Failed to start database services!" -ForegroundColor Red
            Write-Host "Check logs with: docker-compose -f docker-compose.dev.yml logs" -ForegroundColor Yellow
            exit 1
        }
    }
    "3" {
        Write-Host "💻 Local development setup..." -ForegroundColor Yellow
        Write-Host "Starting API + Database services..."
        $result = docker-compose -f docker-compose.dev.yml up -d postgres redis api
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-Host ""
            Write-Host "Installing dependencies..."
            pnpm install
            Write-Host ""
            Write-Host "✅ Ready for hybrid development!" -ForegroundColor Green
            Write-Host "🌐 API: http://localhost:3000 (containerized)"
            Write-Host "📊 PostgreSQL: localhost:5432"
            Write-Host "🔄 Redis: localhost:6379"
            Write-Host ""
            Write-Host "🤖 Test Python AI locally: cd ai-core && python video_ui.py" -ForegroundColor Cyan
            Write-Host "📝 View API logs: docker logs -f queimadai-api-dev" -ForegroundColor Cyan
            
            Write-Host ""
            Write-Host "📊 Container status:" -ForegroundColor Cyan
            docker-compose -f docker-compose.dev.yml ps
        } else {
            Write-Host ""
            Write-Host "❌ Failed to start development services!" -ForegroundColor Red
            Write-Host "Check logs with: docker-compose -f docker-compose.dev.yml logs" -ForegroundColor Yellow
            exit 1
        }
    }
    "4" {
        Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
        docker-compose down -v
        docker-compose -f docker-compose.dev.yml down -v
        Write-Host "✅ All containers and data removed!" -ForegroundColor Green
    }
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📖 For more info, check:" -ForegroundColor Cyan
Write-Host "   - README.md"
Write-Host "   - QUICKSTART.md"
Write-Host "   - docs/DATABASE-STRATEGY.md"

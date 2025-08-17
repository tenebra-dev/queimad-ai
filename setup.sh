#!/bin/bash

# QueimadAI - Setup Script
# Facilita o início do desenvolvimento

echo "🔥 QueimadAI - Development Setup"
echo "================================"

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker found"

# Menu de opções
echo ""
echo "Choose setup option:"
echo "1) 🚀 Full stack (API + AI + Database + Redis)"
echo "2) 🗄️  Only database services (PostgreSQL + Redis + pgAdmin)"
echo "3) 💻 Local development (API + AI local, only DB in Docker)"
echo "4) 🧹 Clean up all containers and data"
echo ""

read -p "Select option (1-4): " option

case $option in
    1)
        echo "🚀 Starting full stack..."
        docker-compose up -d
        echo ""
        echo "✅ Full stack started!"
        echo "🌐 API: http://localhost:3000"
        echo "🤖 AI Core: http://localhost:8000"
        echo "🗄️  pgAdmin: http://localhost:8080 (admin@queimadai.com / admin123)"
        echo "📊 PostgreSQL: localhost:5432"
        echo "🔄 Redis: localhost:6379"
        ;;
    2)
        echo "🗄️  Starting database services only..."
        docker-compose -f docker-compose.dev.yml up -d
        echo ""
        echo "✅ Database services started!"
        echo "🗄️  pgAdmin: http://localhost:8080 (admin@queimadai.com / admin123)"
        echo "📊 PostgreSQL: localhost:5432 (postgres / postgres123)"
        echo "🔄 Redis: localhost:6379"
        echo ""
        echo "💡 Now you can run the API locally with: pnpm dev"
        ;;
    3)
        echo "💻 Local development setup..."
        echo "Starting only database..."
        docker-compose -f docker-compose.dev.yml up -d postgres redis
        echo ""
        echo "Installing dependencies..."
        pnpm install
        echo ""
        echo "✅ Ready for local development!"
        echo "📊 PostgreSQL: localhost:5432"
        echo "🔄 Redis: localhost:6379"
        echo ""
        echo "🚀 Start API with: pnpm dev"
        echo "🤖 Test Python AI: cd ai-core && python video_ui.py"
        ;;
    4)
        echo "🧹 Cleaning up..."
        docker-compose down -v
        docker-compose -f docker-compose.dev.yml down -v
        echo "✅ All containers and data removed!"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "📖 For more info, check:"
echo "   - README.md"
echo "   - QUICKSTART.md"
echo "   - docs/DATABASE-STRATEGY.md"

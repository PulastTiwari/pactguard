#!/bin/bash

# Docker Deployment Script for PactGuard
# Built for AgentHacks2025 by Pulast

echo "🐳 Starting PactGuard Docker Deployment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if environment file exists
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.docker.template .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please update the API keys in .env file if needed"
fi

# Clean up existing containers and images
echo "🧹 Cleaning up existing containers..."
docker-compose down --remove-orphans 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build --no-cache

echo "🚀 Starting PactGuard services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo "🔍 Checking service health..."

# Check backend health
if curl -f http://localhost:8000/health >/dev/null 2>&1; then
    echo "✅ Backend service is healthy (Port 8000)"
else
    echo "❌ Backend service is not responding"
fi

# Check frontend health  
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    echo "✅ Frontend service is healthy (Port 3000)"
else
    echo "❌ Frontend service is not responding"
fi

echo ""
echo "🎉 PactGuard Docker Deployment Complete!"
echo ""
echo "📱 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛠️  Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
echo "🏆 Built for AgentHacks2025 with Portia AI Integration"

# Show container status
echo ""
echo "📊 Container Status:"
docker-compose ps

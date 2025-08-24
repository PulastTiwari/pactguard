#!/bin/bash

# PactGuard Docker Startup Script

echo "🐳 Starting PactGuard with Docker..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.docker.template .env
    echo "📝 Please edit .env file and add your API keys:"
    echo "   - PORTIA_API_KEY: Get from https://app.portialabs.ai/"
    echo "   - GOOGLE_API_KEY: Get from https://makersuite.google.com/app/apikey"
    echo ""
    echo "After adding your keys, run this script again."
    exit 1
fi

# Check if API keys are set
if grep -q "your_portia_api_key_here\|placeholder_portia_api_key" .env; then
    echo "⚠️  Please update PORTIA_API_KEY in .env file"
    echo "   Get your key from: https://app.portialabs.ai/"
    echo ""
fi

if grep -q "your_google_api_key_here\|placeholder_google_api_key" .env; then
    echo "⚠️  Please update GOOGLE_API_KEY in .env file"
    echo "   Get your key from: https://makersuite.google.com/app/apikey"
    echo ""
fi

echo "🔨 Building Docker containers..."
docker-compose build

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Starting PactGuard services..."
    echo ""
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000"
    echo "   Health Check: http://localhost:8000/health"
    echo ""
    echo "Press Ctrl+C to stop all services"
    echo ""
    
    docker-compose up
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi

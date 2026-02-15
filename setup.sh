#!/bin/bash

# Social Media MCP Servers - Quick Setup Script
# Run this once to set up everything

set -e

echo "🚀 Setting up Social Media MCP Servers..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and docker-compose are installed"
echo ""

# Create env files if they don't exist
if [ ! -f .env.facebook ]; then
    echo "📝 Creating .env.facebook from template..."
    cp .env.facebook.example .env.facebook
    echo "   ⚠️  Please edit .env.facebook with your credentials"
else
    echo "✅ .env.facebook already exists"
fi

if [ ! -f .env.linkedin ]; then
    echo "📝 Creating .env.linkedin from template..."
    cp .env.linkedin.example .env.linkedin
    echo "   ⚠️  Please edit .env.linkedin with your credentials"
else
    echo "✅ .env.linkedin already exists"
fi

if [ ! -f .env.telegram ]; then
    echo "📝 Creating .env.telegram from template..."
    cp .env.telegram.example .env.telegram
    echo "   ⚠️  Please edit .env.telegram with your credentials"
else
    echo "✅ .env.telegram already exists"
fi

echo ""
echo "🏗️  Building Docker images..."
docker-compose build

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit your .env files with real credentials:"
echo "      - .env.facebook"
echo "      - .env.linkedin"
echo "      - .env.telegram"
echo ""
echo "   2. Start the servers:"
echo "      docker-compose up -d"
echo ""
echo "   3. View logs:"
echo "      docker-compose logs -f"
echo ""
echo "   4. Test your setup with a simple post!"
echo ""
echo "📖 For detailed usage, see:"
echo "   - SETUP_GUIDE.md"
echo "   - POSTING_REFERENCE.md"
echo ""
echo "🎉 Happy posting!"

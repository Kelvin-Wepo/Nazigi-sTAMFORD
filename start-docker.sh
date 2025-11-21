#!/bin/bash

# 🚀 Quick Start Script for Docker Development
# Nazigi Stamford Bus SMS Service

set -e  # Exit on error

echo "🚌 Nazigi Stamford Bus SMS Service - Docker Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed!${NC}"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed (support both old and new syntax)
DOCKER_COMPOSE_CMD=""
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo -e "${RED}❌ Docker Compose is not installed!${NC}"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"
echo "   Using: $DOCKER_COMPOSE_CMD"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Creating .env from template..."
    cat > .env << 'EOF'
# AfricasTalking Configuration
AT_USERNAME=Kwepo
AT_API_KEY=your_api_key_here
AT_SHORTCODE=20384
AT_SENDER_ID=AFTKNG

# Flask Configuration
SECRET_KEY=local-dev-secret-key-change-in-production
FLASK_ENV=development
DEBUG=True

# Conductor Authentication
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=admin123

# Database (auto-configured by docker-compose)
DATABASE_URL=postgresql://nazigi_user:nazigi2025@db:5432/nazigi_sms

# Python Configuration
PYTHONUNBUFFERED=1
PORT=5000
EOF
    echo -e "${YELLOW}📝 Please edit .env and add your AfricasTalking credentials${NC}"
    echo "   Then run this script again."
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"
echo ""

# Stop any running containers
echo "🛑 Stopping any existing containers..."
$DOCKER_COMPOSE_CMD down 2>/dev/null || true
echo ""

# Build and start services
echo "🔨 Building Docker images..."
$DOCKER_COMPOSE_CMD build
echo ""

echo "🚀 Starting services..."
$DOCKER_COMPOSE_CMD up -d
echo ""

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Check if database is healthy
DB_READY=false
for i in {1..30}; do
    if $DOCKER_COMPOSE_CMD exec -T db pg_isready -U nazigi_user -d nazigi_sms &> /dev/null; then
        DB_READY=true
        break
    fi
    echo "   Waiting for database... ($i/30)"
    sleep 2
done

if [ "$DB_READY" = false ]; then
    echo -e "${RED}❌ Database failed to start${NC}"
    echo "Check logs with: $DOCKER_COMPOSE_CMD logs db"
    exit 1
fi

echo -e "${GREEN}✅ Database is ready${NC}"
echo ""

# Run database migrations
echo "🗄️  Running database migrations..."
$DOCKER_COMPOSE_CMD exec -T web flask db upgrade 2>/dev/null || {
    echo "   Flask-Migrate not initialized, running init_db.py..."
    $DOCKER_COMPOSE_CMD exec -T web python init_db.py
}
echo ""

# Check if services are running
echo "📊 Checking service status..."
$DOCKER_COMPOSE_CMD ps
echo ""

# Get container IP
WEB_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nazigi_flask 2>/dev/null || echo "localhost")

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "=================================================="
echo "🎉 Your application is now running!"
echo "=================================================="
echo ""
echo "📍 Access Points:"
echo "   Dashboard:  http://localhost:5000/conductor/dashboard"
echo "   API:        http://localhost:5000/"
echo "   Callback:   http://localhost:5000/sms/callback"
echo ""
echo "🔐 Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📝 Useful Commands:"
echo "   View logs:          $DOCKER_COMPOSE_CMD logs -f"
echo "   View Flask logs:    $DOCKER_COMPOSE_CMD logs -f web"
echo "   View DB logs:       $DOCKER_COMPOSE_CMD logs -f db"
echo "   Stop services:      $DOCKER_COMPOSE_CMD down"
echo "   Restart Flask:      $DOCKER_COMPOSE_CMD restart web"
echo "   Access shell:       $DOCKER_COMPOSE_CMD exec web bash"
echo "   Access database:    $DOCKER_COMPOSE_CMD exec db psql -U nazigi_user -d nazigi_sms"
echo ""
echo "🧪 Test SMS Callback:"
echo "   curl -X POST http://localhost:5000/sms/callback \\"
echo "     -d \"from=+254799489045\" \\"
echo "     -d \"text=TEXT2\" \\"
echo "     -d \"to=20384\""
echo ""
echo "📚 Documentation:"
echo "   Local Development: LOCAL_DOCKER_GUIDE.md"
echo "   Render Deployment: RENDER_DEPLOYMENT.md"
echo ""
echo -e "${YELLOW}⚠️  For external access (ngrok), run:${NC}"
echo "   ngrok http 5000"
echo ""
echo -e "${GREEN}Happy coding! 🚌✨${NC}"

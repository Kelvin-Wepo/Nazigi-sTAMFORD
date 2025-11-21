# 🐳 Local Docker Development Guide
## Nazigi Stamford Bus SMS Service

Complete guide to run your application locally using Docker and Docker Compose.

---

## 📋 Prerequisites

Install these on your local machine:

- ✅ **Docker** (version 20.10+)
  - Install: https://docs.docker.com/get-docker/
- ✅ **Docker Compose** (version 2.0+)
  - Included with Docker Desktop
- ✅ **Git** (to clone repository)

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone and Navigate to Project

```bash
cd /home/subchief/Nazigi
```

### 2. Create .env File

Make sure your `.env` file exists with proper values:

```bash
# .env should contain:
AT_USERNAME=Kwepo
AT_API_KEY=atsk_6e210a59fcded0df8da23bd3a3ee9f2cfca0d2ec7d560a07a368438b4e403bb673fac5a4
AT_SHORTCODE=20384
AT_SENDER_ID=AFTKNG
SECRET_KEY=your-local-secret-key
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=admin123
```

### 3. Start Everything

```bash
# Build and start all services (Flask + PostgreSQL)
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Initialize Database

In a new terminal:

```bash
# Run database migrations
docker-compose exec web flask db upgrade

# Or run init script
docker-compose exec web python init_db.py
```

### 5. Access Your App

- **Dashboard:** http://localhost:5000/conductor/dashboard
- **API:** http://localhost:5000/
- **Database:** localhost:5432

---

## 🔧 Common Docker Commands

### Start Services

```bash
# Start all services (build if needed)
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Rebuild images and start
docker-compose up --build

# Start only database
docker-compose up db
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes database data!)
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### View Logs

```bash
# Show logs for all services
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Show only Flask app logs
docker-compose logs -f web

# Show only database logs
docker-compose logs -f db
```

### Execute Commands in Containers

```bash
# Open shell in Flask container
docker-compose exec web bash

# Run Python script
docker-compose exec web python view_passengers.py

# Run Flask commands
docker-compose exec web flask db upgrade
docker-compose exec web flask db migrate -m "Add new column"

# Access PostgreSQL
docker-compose exec db psql -U nazigi_user -d nazigi_sms
```

### Check Status

```bash
# List running containers
docker-compose ps

# Check container resource usage
docker stats

# Inspect service details
docker-compose config
```

### Clean Up

```bash
# Remove stopped containers
docker-compose rm

# Remove all unused containers, networks, images
docker system prune

# Remove all unused volumes (WARNING: deletes data!)
docker volume prune
```

---

## 🗄️ Working with Database

### Access PostgreSQL

```bash
# Connect to database
docker-compose exec db psql -U nazigi_user -d nazigi_sms

# Inside psql:
\dt                    # List tables
\d passengers          # Describe passengers table
SELECT * FROM passengers;
\q                     # Quit
```

### Backup Database

```bash
# Create backup
docker-compose exec db pg_dump -U nazigi_user nazigi_sms > backup.sql

# Restore backup
docker-compose exec -T db psql -U nazigi_user -d nazigi_sms < backup.sql
```

### Reset Database

```bash
# Stop services
docker-compose down

# Remove volume (deletes data!)
docker volume rm nazigi_postgres_data

# Restart
docker-compose up -d

# Re-run migrations
docker-compose exec web flask db upgrade
```

---

## 🧪 Testing Locally

### Test SMS Callback

```bash
# Simulate incoming SMS
curl -X POST http://localhost:5000/sms/callback \
  -d "from=+254799489045" \
  -d "text=TEXT2" \
  -d "to=20384"
```

### Test Conductor Dashboard

```bash
# Login and get passengers
curl -u admin:admin123 http://localhost:5000/conductor/passengers

# Send message
curl -X POST http://localhost:5000/conductor/send-message \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

### Run Test Scripts

```bash
# View passengers
docker-compose exec web python view_passengers.py

# Test opt-in flow
docker-compose exec web python test_optin_flow.py

# Clear database
docker-compose exec web python clear_database.py
```

---

## 🔄 Development Workflow

### 1. Make Code Changes

Edit files locally in `/home/subchief/Nazigi/`

```bash
# Files are mounted as volume, changes reflect immediately
# No need to rebuild for Python code changes!
```

### 2. Restart Flask (if needed)

```bash
# Restart just the Flask container
docker-compose restart web

# Or rebuild if you changed Dockerfile
docker-compose up -d --build web
```

### 3. Check Logs

```bash
# Watch logs for your changes
docker-compose logs -f web
```

### 4. Test Changes

```bash
# Run tests
docker-compose exec web python -m pytest

# Or manual tests
curl http://localhost:5000/
```

---

## 🐛 Debugging

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Check if port is already in use
lsof -i :5000
netstat -tuln | grep 5000

# Kill conflicting process
pkill -f "python3 app.py"

# Try starting again
docker-compose up
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Verify DATABASE_URL
docker-compose exec web printenv DATABASE_URL

# Should show: postgresql://nazigi_user:nazigi2025@db:5432/nazigi_sms
```

### Can't Access Database

```bash
# Check database health
docker-compose exec db pg_isready -U nazigi_user

# Try connecting manually
docker-compose exec db psql -U nazigi_user -d nazigi_sms

# If fails, check password in docker-compose.yml
```

### Code Changes Not Reflecting

```bash
# Make sure volumes are mounted
docker-compose config | grep volumes

# Restart Flask
docker-compose restart web

# Or rebuild (for Dockerfile changes)
docker-compose up -d --build web
```

---

## 🔒 Environment Variables

### Load from .env

Docker Compose automatically loads `.env` file.

```bash
# Check what variables are loaded
docker-compose config

# Override specific variable
AT_SHORTCODE=20384 docker-compose up
```

### Add New Variable

1. Add to `.env`:
   ```
   NEW_VAR=value
   ```

2. Add to `docker-compose.yml` under `environment:`:
   ```yaml
   environment:
     NEW_VAR: ${NEW_VAR}
   ```

3. Restart:
   ```bash
   docker-compose down && docker-compose up -d
   ```

---

## 📦 Building Production Image

### Build for Render

```bash
# Test production build locally
docker build -t nazigi-stamford:latest .

# Run production container
docker run -p 5000:5000 \
  -e DATABASE_URL="postgresql://..." \
  -e AT_API_KEY="..." \
  --name nazigi-app \
  nazigi-stamford:latest

# Check logs
docker logs -f nazigi-app
```

---

## 🚀 Tips & Best Practices

### 1. Keep Docker Images Small

```bash
# Check image size
docker images nazigi-stamford

# Remove unused images
docker image prune
```

### 2. Use .dockerignore

Already created! Prevents copying unnecessary files:
- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `.env` - Secrets (use Render environment instead)

### 3. Hot Reload During Development

```bash
# Flask auto-reloads when you save files
# Check docker-compose.yml has --reload flag in command
```

### 4. Database Persistence

```bash
# Data persists in named volume: postgres_data
# Even if you stop containers, data remains

# To completely reset:
docker-compose down -v  # WARNING: Deletes data!
```

### 5. Monitor Resource Usage

```bash
# Check memory/CPU usage
docker stats

# Limit resources in docker-compose.yml:
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

---

## 🆘 Common Issues

### Port Already in Use

```bash
# Error: "port is already allocated"
# Solution 1: Kill process using port
lsof -ti:5000 | xargs kill -9

# Solution 2: Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use host port 5001 instead
```

### Permission Denied

```bash
# Error: "permission denied while trying to connect to Docker daemon"
# Solution: Add user to docker group
sudo usermod -aG docker $USER

# Then logout and login again
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a --volumes

# Check disk usage
docker system df
```

---

## ✅ Local Development Checklist

Before starting development:

- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] `.env` file created with proper values
- [ ] Ports 5000 and 5432 not in use
- [ ] Git repository up to date

Daily workflow:

- [ ] `docker-compose up -d` - Start services
- [ ] Make code changes
- [ ] `docker-compose logs -f web` - Watch logs
- [ ] Test changes locally
- [ ] `docker-compose down` - Stop when done

---

## 📚 Additional Resources

- Docker Docs: https://docs.docker.com/
- Docker Compose Docs: https://docs.docker.com/compose/
- Flask in Docker: https://flask.palletsprojects.com/en/2.3.x/deploying/docker/
- PostgreSQL in Docker: https://hub.docker.com/_/postgres

---

**Happy Dockerizing! 🐳🚌**

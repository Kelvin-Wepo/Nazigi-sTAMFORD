# 🐳 Docker Deployment Summary
## Nazigi Stamford Bus SMS Service

Quick reference for all Docker and Render deployment commands and configurations.

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `Dockerfile` | Production Docker image configuration |
| `docker-compose.yml` | Local development environment setup |
| `.dockerignore` | Files to exclude from Docker builds |
| `render.yaml` | Render Blueprint for one-click deployment |
| `start-docker.sh` | Automated setup script for local Docker |
| `RENDER_DEPLOYMENT.md` | Complete Render deployment guide |
| `LOCAL_DOCKER_GUIDE.md` | Complete local Docker development guide |

---

## 🚀 Quick Commands

### Local Development (Docker)

```bash
# One-command setup (recommended)
./start-docker.sh

# Manual setup
docker-compose up -d --build
docker-compose exec web flask db upgrade

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Reset everything (WARNING: deletes data)
docker-compose down -v
```

### Test Locally

```bash
# Test SMS callback
curl -X POST http://localhost:5000/sms/callback \
  -d "from=+254799489045" \
  -d "text=TEXT2" \
  -d "to=20384"

# Test dashboard
curl -u admin:admin123 http://localhost:5000/conductor/dashboard

# Access database
docker-compose exec db psql -U nazigi_user -d nazigi_sms
```

---

## 🌐 Render Deployment

### Option 1: Using Render Blueprint (Easiest)

1. Push code to GitHub:
   ```bash
   git add Dockerfile docker-compose.yml .dockerignore render.yaml
   git commit -m "Add Docker and Render deployment files"
   git push origin main
   ```

2. Go to Render Dashboard: https://dashboard.render.com/
3. Click **"New"** → **"Blueprint"**
4. Connect repository: `Kelvin-Wepo/Nazigi-sTAMFORD`
5. Render will create PostgreSQL + Web Service automatically
6. Add environment variables manually (see below)

### Option 2: Manual Setup

1. Create PostgreSQL database on Render
2. Create Web Service (Docker runtime)
3. Connect GitHub repository
4. Set environment variables
5. Deploy

### Required Environment Variables on Render

```bash
# Flask
FLASK_ENV=production
SECRET_KEY=generate-random-32-char-string
DEBUG=False
PORT=10000
PYTHONUNBUFFERED=1

# Database (auto-set if using render.yaml)
DATABASE_URL=postgresql://user:pass@host.internal:5432/nazigi_sms

# AfricasTalking
AT_USERNAME=Kwepo
AT_API_KEY=atsk_6e210a59fcded0df8da23bd3a3ee9f2cfca0d2ec7d560a07a368438b4e403bb673fac5a4
AT_SHORTCODE=20384
AT_SENDER_ID=AFTKNG

# Conductor Auth
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=change-this-strong-password
```

### After Deployment

1. Open Render Shell (Web Service → Shell tab)
2. Run migrations:
   ```bash
   flask db upgrade
   # Or
   python init_db.py
   ```

3. Update AfricasTalking callback:
   ```
   https://your-app-name.onrender.com/sms/callback
   ```

---

## 🏗️ Dockerfile Explained

```dockerfile
FROM python:3.10-slim                    # Small base image
ENV PYTHONUNBUFFERED=1                   # Enable real-time logs
RUN apt-get install gcc libpq-dev        # PostgreSQL dependencies
COPY requirements.txt .                  # Copy dependencies first (caching)
RUN pip install -r requirements.txt      # Install Python packages
COPY . .                                 # Copy application code
USER appuser                             # Run as non-root (security)
CMD gunicorn -b 0.0.0.0:$PORT app:app   # Start with Gunicorn
```

**Key Features:**
- ✅ Multi-stage efficient caching
- ✅ Non-root user for security
- ✅ Health checks included
- ✅ Production Gunicorn configuration
- ✅ 4 workers, 2 threads per worker
- ✅ 120s timeout for long SMS operations

---

## 🔍 Troubleshooting

### Issue: Docker build fails with "gcc: command not found"

**Solution:** The Dockerfile installs gcc. If it still fails:
```bash
# In Dockerfile, change:
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential
```

### Issue: Database connection refused

**Solution:**
```bash
# Check DATABASE_URL format
# Local: postgresql://nazigi_user:nazigi2025@db:5432/nazigi_sms
# Render: postgresql://user:pass@host.internal:5432/nazigi_sms

# Check database is running
docker-compose ps db
docker-compose logs db
```

### Issue: Port already in use

**Solution:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "5001:5000"
```

### Issue: Code changes not reflecting

**Solution:**
```bash
# For Python code changes (no rebuild needed)
docker-compose restart web

# For Dockerfile changes (rebuild needed)
docker-compose up -d --build web

# For dependency changes (rebuild needed)
docker-compose down
docker-compose up -d --build
```

### Issue: Authentication error on Render

**Error:** `The supplied authentication is invalid`

**Solution:**
```bash
# Check environment variables in Render dashboard
# Verify AT_API_KEY is correct (no spaces, quotes)
# Ensure all required env vars are set

# Test locally first
docker-compose exec web python -c "
from sms_service import SMSService
import os
print(f'Username: {os.getenv(\"AT_USERNAME\")}')
print(f'API Key: {os.getenv(\"AT_API_KEY\")[:10]}...')
"
```

### Issue: Render app crashes on startup

**Solution:**
```bash
# Check Render logs (Logs tab)
# Common issues:
# 1. Missing environment variables
# 2. Database not ready
# 3. Port not set correctly

# Verify DATABASE_URL format
# Must be: postgresql://user:pass@host.internal:5432/dbname
```

### Issue: SMS not received

**Solution:**
```bash
# 1. Check AfricasTalking callback URL
# Must be: https://your-app.onrender.com/sms/callback

# 2. Check Render logs for incoming SMS
# Should see: 📥 ========== INCOMING SMS ==========

# 3. Verify AfricasTalking balance
# Dashboard → Account Balance

# 4. Test manually
curl -X POST https://your-app.onrender.com/sms/callback \
  -d "from=+254799489045" \
  -d "text=TEST2" \
  -d "to=20384"
```

---

## 📊 Monitoring

### View Logs

```bash
# Local Docker
docker-compose logs -f web
docker-compose logs -f db

# Render
# Web Service → Logs tab (real-time logs)
```

### Check Health

```bash
# Local
curl http://localhost:5000/

# Render
curl https://your-app.onrender.com/
```

### Database Queries

```bash
# Local Docker
docker-compose exec db psql -U nazigi_user -d nazigi_sms -c "SELECT COUNT(*) FROM passengers;"

# Render (via Shell)
psql $DATABASE_URL -c "SELECT COUNT(*) FROM passengers;"
```

---

## 🔒 Security Checklist

Before production deployment:

- [ ] Change `SECRET_KEY` to random 32+ character string
- [ ] Change `CONDUCTOR_PASSWORD` from default
- [ ] Never commit `.env` to Git (already in `.gitignore`)
- [ ] Use Render's environment variables (not hardcoded)
- [ ] Enable HTTPS (Render does this automatically)
- [ ] Set strong database password
- [ ] Rotate API keys every 90 days
- [ ] Monitor logs for suspicious activity
- [ ] Use Render's Internal Database URL (free bandwidth)
- [ ] Set up Render's health checks
- [ ] Enable Render's auto-deploy from GitHub

---

## 📈 Performance Optimization

### Gunicorn Configuration

Current settings in `Dockerfile`:
```bash
gunicorn --workers 4        # 4 worker processes
         --threads 2        # 2 threads per worker
         --timeout 120      # 120s timeout for SMS callbacks
```

**For high traffic:**
```bash
# Increase workers
--workers 6

# Increase threads
--threads 4

# Use gevent for async
--worker-class gevent
--worker-connections 1000
```

### Database Connection Pool

Add to `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,           # Max connections in pool
    "max_overflow": 20,        # Additional connections if pool full
    "pool_timeout": 30,        # Wait 30s for connection
    "pool_recycle": 1800,      # Recycle connections after 30 min
}
```

### Docker Image Size

```bash
# Check image size
docker images nazigi-stamford

# Optimize by:
# 1. Using python:3.10-slim (already done)
# 2. Multi-stage builds (can be added)
# 3. Removing build dependencies after install
```

---

## 🔄 CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Trigger Render Deploy
        run: |
          curl -X POST \
            "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```

Get Deploy Hook URL from: Render → Web Service → Settings → Deploy Hook

---

## 📚 Next Steps

1. **Test locally:**
   ```bash
   ./start-docker.sh
   ```

2. **Deploy to Render:**
   - Follow `RENDER_DEPLOYMENT.md`

3. **Configure AfricasTalking:**
   - Update callback URL to Render app URL

4. **Monitor:**
   - Check Render logs daily
   - Monitor AfricasTalking SMS logs
   - Track database size

5. **Scale as needed:**
   - Upgrade Render plan for more resources
   - Increase Gunicorn workers
   - Add caching layer (Redis)

---

## 📞 Support

- **Local Docker Issues:** See `LOCAL_DOCKER_GUIDE.md`
- **Render Deployment Issues:** See `RENDER_DEPLOYMENT.md`
- **Application Issues:** Check Flask logs
- **SMS Issues:** Check AfricasTalking logs

---

## ✅ Deployment Verification Checklist

After deployment:

- [ ] App accessible at Render URL
- [ ] Database connected (check dashboard)
- [ ] All environment variables set
- [ ] Database migrations run successfully
- [ ] AfricasTalking callback URL updated
- [ ] SMS registration flow works (send TEXT2 to 20384)
- [ ] Conductor dashboard accessible
- [ ] Test sending bulk message
- [ ] Logs showing proper emoji formatting
- [ ] Health checks passing
- [ ] Auto-deploy enabled (optional)

---

**You're all set! 🎉**

Run `./start-docker.sh` to get started locally, then follow `RENDER_DEPLOYMENT.md` to deploy to production.

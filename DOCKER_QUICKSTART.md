# 🚀 QUICK START: Docker & Render Deployment

## Two Commands to Get Started

### 1️⃣ Test Locally (1 minute)

```bash
cd /home/subchief/Nazigi
./start-docker.sh
```

✅ This will:
- Build Docker images
- Start PostgreSQL + Flask
- Run database migrations
- Show you access URLs

**Test it:** http://localhost:5000/conductor/dashboard (admin/admin123)

---

### 2️⃣ Deploy to Production (10 minutes)

#### A. Push to GitHub

```bash
git add Dockerfile docker-compose.yml .dockerignore render.yaml
git commit -m "Add Docker and Render deployment"
git push origin main
```

#### B. Deploy on Render

1. Go to https://dashboard.render.com/
2. Click **"New"** → **"Web Service"**
3. Connect repository: `Kelvin-Wepo/Nazigi-sTAMFORD`
4. Select:
   - **Runtime:** Docker
   - **Region:** Singapore (or closest to you)
   - **Plan:** Starter ($7/mo recommended)
5. Add environment variables (see below)
6. Click **"Create Web Service"**

#### C. Environment Variables (Add in Render Dashboard)

```bash
FLASK_ENV=production
SECRET_KEY=generate-random-32-char-string
DEBUG=False
DATABASE_URL=postgresql://user:pass@host.internal:5432/nazigi_sms
AT_USERNAME=Kwepo
AT_API_KEY=atsk_6e210a59fcded0df8da23bd3a3ee9f2cfca0d2ec7d560a07a368438b4e403bb673fac5a4
AT_SHORTCODE=20384
AT_SENDER_ID=AFTKNG
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=strong-password-here
PYTHONUNBUFFERED=1
```

#### D. After Deployment

```bash
# 1. In Render Shell (Web Service → Shell tab):
flask db upgrade

# 2. Update AfricasTalking callback URL to:
https://your-app-name.onrender.com/sms/callback

# 3. Test: Send "TEXT2" to 20384
```

**Done! 🎉**

---

## 📁 What Was Created?

| File | Purpose |
|------|---------|
| `Dockerfile` | Production Docker image |
| `docker-compose.yml` | Local development environment |
| `.dockerignore` | Optimize Docker builds |
| `render.yaml` | One-click Render deployment |
| `start-docker.sh` | Automated local setup |
| `RENDER_DEPLOYMENT.md` | Complete Render guide (read this!) |
| `LOCAL_DOCKER_GUIDE.md` | Docker development guide |
| `DOCKER_SUMMARY.md` | Quick command reference |
| `DEPLOYMENT_CHECKLIST.md` | Step-by-step checklist |

---

## 🔥 Common Commands

```bash
# Start local Docker
./start-docker.sh

# View logs
docker-compose logs -f web

# Stop everything
docker-compose down

# Reset database (WARNING: deletes data)
docker-compose down -v

# Test SMS callback
curl -X POST http://localhost:5000/sms/callback \
  -d "from=+254799489045" \
  -d "text=TEST2" \
  -d "to=20384"

# Access database
docker-compose exec db psql -U nazigi_user -d nazigi_sms

# Run tests in container
docker-compose exec web python view_passengers.py
```

---

## 🎯 What You Get

### ✅ Production-Ready Docker Setup
- Multi-stage efficient builds
- Non-root user security
- Health checks included
- Optimized for Render

### ✅ Complete Deployment Pipeline
- Local development with docker-compose
- One-command setup script
- Auto-deploy from GitHub
- PostgreSQL database included

### ✅ Comprehensive Documentation
- 5 detailed guides
- Step-by-step checklist
- Troubleshooting section
- Best practices included

---

## 🚨 Important Notes

### ⚠️ Before Deploying:

1. **Never commit .env to Git**
   - Already in `.gitignore`
   - Set variables in Render dashboard

2. **Change default passwords**
   - `CONDUCTOR_PASSWORD` must be strong
   - `SECRET_KEY` must be random 32+ chars

3. **Use Internal Database URL**
   - Format: `postgresql://user:pass@host.internal:5432/db`
   - Saves bandwidth costs on Render

4. **Update AfricasTalking callback**
   - Must point to your Render app URL
   - Format: `https://your-app.onrender.com/sms/callback`

---

## 📚 Next Steps

### First Time Setup:

1. **Read:** `DEPLOYMENT_CHECKLIST.md` (comprehensive guide)
2. **Test Locally:** Run `./start-docker.sh`
3. **Deploy:** Follow `RENDER_DEPLOYMENT.md`
4. **Verify:** Complete checklist in `DEPLOYMENT_CHECKLIST.md`

### Daily Development:

1. **Start:** `docker-compose up -d`
2. **Code:** Edit files (auto-reloads)
3. **Test:** Check http://localhost:5000
4. **Stop:** `docker-compose down`

### Deployment Updates:

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main

# Render auto-deploys (if enabled)
# Or manually deploy in Render dashboard
```

---

## 🆘 Troubleshooting

### Local Docker Issues

**Problem:** Port 5000 already in use  
**Solution:**
```bash
lsof -ti:5000 | xargs kill -9
docker-compose down
docker-compose up -d
```

**Problem:** Database won't start  
**Solution:**
```bash
docker-compose down -v  # Deletes database!
docker-compose up -d
docker-compose exec web flask db upgrade
```

### Render Deployment Issues

**Problem:** Build fails  
**Solution:**
- Check Render logs (Logs tab)
- Verify all environment variables set
- Ensure Dockerfile syntax correct

**Problem:** Database connection error  
**Solution:**
- Use Internal Database URL (ends with `.internal`)
- Format: `postgresql://user:pass@host.internal:5432/db`
- Verify DATABASE_URL in environment variables

**Problem:** SMS not received  
**Solution:**
- Update AfricasTalking callback URL
- Check Render logs for incoming SMS (📥 icon)
- Verify AfricasTalking account balance
- Test with curl first

---

## ✅ Verification Tests

After deployment, verify everything works:

```bash
# 1. Health check
curl https://your-app.onrender.com/

# 2. Test callback
curl -X POST https://your-app.onrender.com/sms/callback \
  -d "from=+254799489045" \
  -d "text=TEST2" \
  -d "to=20384"

# 3. Test dashboard (in browser)
https://your-app.onrender.com/conductor/dashboard

# 4. Live SMS test
# Send "TEXT2" to 20384 from your phone
```

---

## 🎊 Success Criteria

You've successfully deployed when:

- ✅ Local Docker runs: `./start-docker.sh` works
- ✅ Render app live: https://your-app.onrender.com/ loads
- ✅ Database connected: Dashboard shows stats
- ✅ SMS works: "TEXT2" to 20384 gets response
- ✅ Dashboard accessible: Can login and send messages
- ✅ Logs working: Can see emoji indicators in Render logs

---

## 📞 Support

- **Detailed Guides:** Read `RENDER_DEPLOYMENT.md` and `LOCAL_DOCKER_GUIDE.md`
- **Step-by-Step:** Follow `DEPLOYMENT_CHECKLIST.md`
- **Quick Reference:** Check `DOCKER_SUMMARY.md`
- **Render Docs:** https://render.com/docs/docker
- **AfricasTalking Docs:** https://developers.africastalking.com/

---

## 🏆 You're Ready!

Everything is set up and ready to deploy. Choose your path:

### 🔵 Local Development First?
```bash
./start-docker.sh
```
Then read: `LOCAL_DOCKER_GUIDE.md`

### 🟢 Deploy to Production Now?
Read: `RENDER_DEPLOYMENT.md` or `DEPLOYMENT_CHECKLIST.md`

### 📋 Want a Checklist?
Follow: `DEPLOYMENT_CHECKLIST.md` (recommended!)

---

**Happy deploying! 🚀🚌📱**

*Your Nazigi Stamford Bus SMS Service is production-ready!*

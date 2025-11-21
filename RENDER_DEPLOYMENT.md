# 🚀 Render Deployment Guide
## Nazigi Stamford Bus SMS Service

Complete step-by-step instructions to deploy your Dockerized Flask application on Render.

---

## 📋 Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account with your code pushed to a repository
- ✅ Render account (sign up at https://render.com)
- ✅ AfricasTalking account with API credentials
- ✅ All local tests passing
- ✅ Docker and docker-compose working locally

---

## 🗄️ Step 1: Create PostgreSQL Database on Render

### 1.1 Create Database

1. Log into Render Dashboard: https://dashboard.render.com/
2. Click **"New"** → **"PostgreSQL"**
3. Configure database:
   ```
   Name: nazigi-postgres
   Database: nazigi_sms
   User: nazigi_user
   Region: Choose closest to your users (e.g., Singapore, Frankfurt, Ohio)
   PostgreSQL Version: 14
   Plan: Free (or Starter for production)
   ```
4. Click **"Create Database"**

### 1.2 Save Database Credentials

After creation, Render shows:
```
Internal Database URL: postgresql://nazigi_user:xxx@xxx-postgres.internal:5432/nazigi_sms
External Database URL: postgresql://nazigi_user:xxx@xxx.oregon-postgres.render.com:5432/nazigi_sms
```

**Copy the Internal Database URL** - this is what your app will use.

---

## 🐳 Step 2: Deploy Flask App as Docker Web Service

### 2.1 Push Code to GitHub

Make sure your code is pushed with Dockerfile:

```bash
cd /home/subchief/Nazigi
git add Dockerfile .dockerignore docker-compose.yml
git commit -m "Add Docker configuration for Render deployment"
git push origin main
```

### 2.2 Create Web Service on Render

1. Go to Render Dashboard
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Select **"Kelvin-Wepo/Nazigi-sTAMFORD"** repository
4. Configure service:

   ```
   Name: nazigi-stamford-sms
   Region: Same as database (important for latency)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Docker
   ```

5. **Instance Type:**
   - Free tier: For testing only (spins down after 15 min inactivity)
   - Starter ($7/mo): Recommended for production (always on)

6. Click **"Create Web Service"**

---

## ⚙️ Step 3: Configure Environment Variables

In your Render Web Service dashboard, go to **"Environment"** tab and add these variables:

### Required Variables

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-min-32-chars
DEBUG=False
PORT=10000

# Database (use Internal Database URL from Step 1.2)
DATABASE_URL=postgresql://nazigi_user:PASSWORD@xxx-postgres.internal:5432/nazigi_sms

# AfricasTalking Credentials
AT_USERNAME=Kwepo
AT_API_KEY=atsk_6e210a59fcded0df8da23bd3a3ee9f2cfca0d2ec7d560a07a368438b4e403bb673fac5a4
AT_SHORTCODE=20384
AT_SENDER_ID=AFTKNG

# Conductor Authentication (change in production!)
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=strong-password-here-not-admin123

# Python Configuration
PYTHONUNBUFFERED=1
```

### Important Notes:
- ⚠️ **Never commit .env to Git** - Set these in Render dashboard only
- 🔐 Change `SECRET_KEY` to a random 32+ character string
- 🔑 Change `CONDUCTOR_PASSWORD` to something secure
- 📊 Use the **Internal Database URL** (faster, free bandwidth)
- 🔢 `PORT` is set by Render automatically, but define as 10000 as fallback

---

## 🗃️ Step 4: Run Database Migrations

After first deployment, you need to initialize the database:

### 4.1 Access Render Shell

1. Go to your Web Service dashboard
2. Click **"Shell"** tab (top right)
3. This opens a terminal in your running container

### 4.2 Run Migrations

```bash
# Initialize database tables
flask db upgrade

# Or if migrations don't exist yet, run init script
python init_db.py
```

### 4.3 Verify Database

```bash
# Check if tables were created
python -c "from app import create_app, db; from models import Passenger; app=create_app(); app.app_context().push(); print(f'Passengers: {Passenger.query.count()}')"
```

Expected output: `Passengers: 0` (or your current count)

---

## 🌐 Step 5: Get Your App URL

After deployment completes, Render assigns a public URL:

```
https://nazigi-stamford-sms.onrender.com
```

### Test Endpoints:

```bash
# Home page
curl https://nazigi-stamford-sms.onrender.com/

# Dashboard (with auth)
curl -u admin:your-password https://nazigi-stamford-sms.onrender.com/conductor/dashboard

# SMS Callback (this is what AfricasTalking will call)
https://nazigi-stamford-sms.onrender.com/sms/callback
```

---

## 📱 Step 6: Configure AfricasTalking Callback

### 6.1 Set Callback URL

1. Log into AfricasTalking: https://account.africastalking.com/
2. Navigate to: **SMS** → **Settings** → **Callback URLs**
3. Set **Incoming Messages Callback URL** to:
   ```
   https://nazigi-stamford-sms.onrender.com/sms/callback
   ```
4. HTTP Method: **POST**
5. Click **"Save"**

### 6.2 Configure Keyword

1. Go to: **SMS** → **Keywords**
2. Verify keyword **TEST2** is mapped to shortcode **20384**
3. Set Callback URL: Same as above

---

## 🧪 Step 7: Test the Complete Flow

### 7.1 Test SMS Registration

From your phone:
1. Send: `TEXT2` to `20384`
2. You should receive: "Welcome to Nazigi Stamford! Would you like to opt? Reply: 1 to Opt In, 2 to Opt Out"
3. Reply: `1`
4. You should receive: "Thank you for opting in! ✅..."

### 7.2 Test Conductor Dashboard

1. Open: `https://nazigi-stamford-sms.onrender.com/conductor/dashboard`
2. Login: `admin` / `your-password`
3. Send a test message
4. Verify your phone receives it with stop selection menu

### 7.3 Check Logs

In Render dashboard:
- Click **"Logs"** tab
- You should see emoji indicators:
  ```
  📥 ========== INCOMING SMS ==========
  📱 From: +254799489045
  💬 Text: TEXT2
  ```

---

## 🔧 Step 8: Production Optimizations

### 8.1 Enable Auto-Deploy

Render can auto-deploy when you push to GitHub:
1. Go to **"Settings"** → **"Build & Deploy"**
2. Enable **"Auto-Deploy"**: Yes
3. Branch: main

### 8.2 Set Health Check

Add health check path in Render:
1. Go to **"Settings"** → **"Health Check"**
2. Path: `/`
3. This ensures Render restarts your app if it crashes

### 8.3 Monitor Performance

- **Logs**: Real-time logs in Render dashboard
- **Metrics**: Check CPU/Memory usage
- **Alerts**: Set up email notifications for downtime

---

## 📊 Common Issues & Solutions

### Issue 1: App Won't Start

**Symptoms:** 
- Logs show: `ERROR: Could not connect to database`
- Build fails

**Solutions:**
```bash
# Check DATABASE_URL format
postgresql://user:password@host:5432/database

# Verify database is running
# In Render: Check PostgreSQL service status

# Check environment variables
# In Render: Environment tab → verify all required vars set
```

### Issue 2: SMS Not Received

**Symptoms:**
- AfricasTalking shows "Failed to deliver"
- Status Code 100 but message not arriving

**Solutions:**
```bash
# 1. Check callback URL is correct
https://your-app.onrender.com/sms/callback

# 2. Verify AfricasTalking balance
# Dashboard → Account Balance → Top up if low

# 3. Check Render logs for incoming SMS
# Logs tab → Search for "📥 INCOMING SMS"

# 4. Test callback manually
curl -X POST https://your-app.onrender.com/sms/callback \
  -d "from=+254799489045" \
  -d "text=TEST2" \
  -d "to=20384"
```

### Issue 3: Slow Response Times

**Symptoms:**
- SMS delayed by 30+ seconds
- Dashboard loads slowly

**Solutions:**
```bash
# 1. Check database region matches app region
# Both should be in same datacenter

# 2. Upgrade instance type
# Free tier spins down after 15 min → Use Starter plan

# 3. Increase Gunicorn workers
# In Dockerfile, change: --workers 4 to --workers 6
```

### Issue 4: Database Connection Pool Exhausted

**Symptoms:**
- Logs show: `FATAL: sorry, too many clients already`

**Solutions:**
```python
# In config.py, add connection pool settings:
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "max_overflow": 20,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` to Git
- ✅ Use Render's environment variable manager
- ✅ Rotate API keys every 90 days
- ✅ Use strong passwords (20+ chars)

### 2. HTTPS
- ✅ Render provides free SSL automatically
- ✅ Always use HTTPS for callbacks
- ✅ Verify SSL certificates

### 3. Rate Limiting
Consider adding rate limiting to prevent abuse:

```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/sms/callback', methods=['POST'])
@limiter.limit("10 per minute")
def sms_callback():
    # ...
```

---

## 📈 Monitoring & Maintenance

### Daily Checks
- ✅ Check Render dashboard for errors
- ✅ Monitor AfricasTalking SMS logs
- ✅ Verify passenger count growing

### Weekly Checks
- ✅ Review database size (Render shows this)
- ✅ Check account balance (AfricasTalking)
- ✅ Review error logs for patterns

### Monthly Checks
- ✅ Rotate API keys
- ✅ Update dependencies: `pip install --upgrade -r requirements.txt`
- ✅ Review and optimize database queries
- ✅ Backup database (Render does this automatically)

---

## 🆘 Support & Resources

### Render Documentation
- https://render.com/docs
- https://render.com/docs/docker
- https://render.com/docs/databases

### AfricasTalking Documentation
- https://developers.africastalking.com/docs/sms/overview
- https://developers.africastalking.com/docs/sms/sending

### Your App Endpoints
```
Dashboard:  https://nazigi-stamford-sms.onrender.com/conductor/dashboard
Callback:   https://nazigi-stamford-sms.onrender.com/sms/callback
API Docs:   https://nazigi-stamford-sms.onrender.com/
```

---

## ✅ Deployment Checklist

Before going live:

- [ ] Database created on Render
- [ ] Web Service deployed successfully
- [ ] All environment variables configured
- [ ] Database migrations run
- [ ] AfricasTalking callback URL updated
- [ ] Tested SMS registration flow
- [ ] Tested conductor dashboard
- [ ] Tested stop selection
- [ ] Checked logs for errors
- [ ] Updated production passwords
- [ ] AfricasTalking account topped up
- [ ] Auto-deploy enabled
- [ ] Health checks configured
- [ ] Monitoring alerts set up

---

## 🎉 You're Live!

Your Nazigi Stamford Bus SMS Service is now running on Render!

**Test it:**
1. Send `TEXT2` to `20384` from your phone
2. Check Render logs
3. Verify you receive SMS responses

**Next Steps:**
- Monitor logs for the first 24 hours
- Gather feedback from conductors
- Scale up as passenger count grows

**Need Help?**
- Check Render logs first
- Review AfricasTalking SMS logs
- Check this guide's troubleshooting section

---

**Good luck with your deployment! 🚀🚌**

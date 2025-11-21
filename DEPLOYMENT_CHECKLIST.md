# ✅ Complete Docker & Render Deployment Checklist
## Nazigi Stamford Bus SMS Service

Use this checklist to ensure successful deployment from local Docker to Render production.

---

## 📋 Pre-Deployment Checklist

### Local Environment Setup

- [ ] Docker installed (version 20.10+)
  ```bash
  docker --version
  ```

- [ ] Docker Compose installed (version 2.0+)
  ```bash
  docker-compose --version
  ```

- [ ] Git repository up to date
  ```bash
  git status
  git pull origin main
  ```

- [ ] All required files present:
  - [ ] `Dockerfile`
  - [ ] `docker-compose.yml`
  - [ ] `.dockerignore`
  - [ ] `render.yaml`
  - [ ] `start-docker.sh`
  - [ ] `requirements.txt` (with gunicorn==21.2.0)
  - [ ] `.env` file (with your credentials)

### Environment Variables Ready

Create a `.env` file with these values:

- [ ] `AT_USERNAME` - AfricasTalking username
- [ ] `AT_API_KEY` - AfricasTalking API key
- [ ] `AT_SHORTCODE` - Your shortcode (20384)
- [ ] `AT_SENDER_ID` - Approved sender ID (AFTKNG)
- [ ] `SECRET_KEY` - Random 32+ character string
- [ ] `CONDUCTOR_USERNAME` - Admin username
- [ ] `CONDUCTOR_PASSWORD` - Strong password
- [ ] `DATABASE_URL` - PostgreSQL connection string

---

## 🐳 Local Docker Testing

### 1. Initial Setup

- [ ] Run automated setup script:
  ```bash
  cd /home/subchief/Nazigi
  ./start-docker.sh
  ```

- [ ] Verify services started:
  ```bash
  docker-compose ps
  ```
  Should show:
  - `nazigi_flask` - Status: Up
  - `nazigi_postgres` - Status: Up (healthy)

### 2. Database Verification

- [ ] Check database connection:
  ```bash
  docker-compose exec web python -c "from app import db; print('DB Connected!')"
  ```

- [ ] Verify tables created:
  ```bash
  docker-compose exec db psql -U nazigi_user -d nazigi_sms -c "\dt"
  ```
  Should show: passengers, conductor_messages, passenger_responses, sms_logs

- [ ] Check passenger count:
  ```bash
  docker-compose exec db psql -U nazigi_user -d nazigi_sms -c "SELECT COUNT(*) FROM passengers;"
  ```

### 3. Application Testing

- [ ] Test home page:
  ```bash
  curl http://localhost:5000/
  ```
  Should return HTML with "Nazigi Stamford Bus SMS Service"

- [ ] Test conductor dashboard (in browser):
  - Open: http://localhost:5000/conductor/dashboard
  - Login: admin / admin123
  - Should see dashboard with statistics

- [ ] Test SMS callback endpoint:
  ```bash
  curl -X POST http://localhost:5000/sms/callback \
    -d "from=+254799489045" \
    -d "text=TEST2" \
    -d "to=20384"
  ```
  Should return: `{"status":"success","message":"Processed"}`

- [ ] Check logs for emoji indicators:
  ```bash
  docker-compose logs web | tail -20
  ```
  Should see: 📥 ========== INCOMING SMS ==========

### 4. End-to-End SMS Flow Test

Using AfricasTalking (with ngrok for callback):

- [ ] Start ngrok:
  ```bash
  ngrok http 5000
  ```

- [ ] Get ngrok URL (e.g., https://abc123.ngrok-free.app)

- [ ] Update AfricasTalking callback URL:
  - Dashboard → SMS → Settings → Callback URLs
  - Set to: `https://abc123.ngrok-free.app/sms/callback`

- [ ] Test SMS registration:
  - Send "TEXT2" to 20384
  - [ ] Receive welcome message
  - Reply "1" to opt in
  - [ ] Receive confirmation message

- [ ] Test stop selection:
  - Send bulk message from dashboard
  - [ ] Receive message with stop list
  - Reply "5" (Zimmerman)
  - [ ] Receive confirmation

- [ ] Verify in dashboard:
  - [ ] Passenger count increased
  - [ ] Response recorded
  - [ ] Analytics updated

### 5. Clean Up Local Test

- [ ] Stop services:
  ```bash
  docker-compose down
  ```

- [ ] Remove test data (optional):
  ```bash
  docker-compose down -v
  ```

---

## 🚀 GitHub & Render Preparation

### 1. Commit Docker Files

- [ ] Stage Docker files:
  ```bash
  git add Dockerfile docker-compose.yml .dockerignore render.yaml
  git add start-docker.sh RENDER_DEPLOYMENT.md LOCAL_DOCKER_GUIDE.md DOCKER_SUMMARY.md
  git add DEPLOYMENT_CHECKLIST.md
  ```

- [ ] Commit with message:
  ```bash
  git commit -m "Add Docker and Render deployment configuration

  - Production-ready Dockerfile with Gunicorn
  - docker-compose.yml for local development
  - .dockerignore for efficient builds
  - render.yaml for Blueprint deployment
  - Comprehensive deployment guides
  - Automated setup script"
  ```

- [ ] Push to GitHub:
  ```bash
  git push origin main
  ```

- [ ] Verify on GitHub:
  - Check all files visible in repository
  - Ensure `.env` is NOT pushed (should be in .gitignore)

### 2. Render Account Setup

- [ ] Sign up for Render: https://render.com/
- [ ] Verify email address
- [ ] Connect GitHub account:
  - Dashboard → Account Settings → Connected Accounts → GitHub
  - Authorize Render

---

## 🗄️ Render Database Setup

### 1. Create PostgreSQL Database

- [ ] Go to Render Dashboard
- [ ] Click "New" → "PostgreSQL"
- [ ] Configure:
  - **Name:** `nazigi-postgres`
  - **Database:** `nazigi_sms`
  - **User:** `nazigi_user`
  - **Region:** Choose closest to users (e.g., Singapore, Frankfurt, Ohio)
  - **PostgreSQL Version:** 14
  - **Plan:** Free (or Starter for production)

- [ ] Click "Create Database"

- [ ] Wait for provisioning (~2 minutes)

### 2. Save Database Credentials

- [ ] Copy **Internal Database URL**:
  ```
  postgresql://nazigi_user:xxx@xxx-postgres.internal:5432/nazigi_sms
  ```
  ⚠️ Use Internal URL (not External) for free bandwidth

- [ ] Save to secure location (password manager)

---

## 🌐 Render Web Service Setup

### 1. Create Web Service

- [ ] Go to Render Dashboard
- [ ] Click "New" → "Web Service"
- [ ] Connect repository:
  - Click "Connect account" if needed
  - Select `Kelvin-Wepo/Nazigi-sTAMFORD`
  - Click "Connect"

- [ ] Configure service:
  - **Name:** `nazigi-stamford-sms`
  - **Region:** Same as database (IMPORTANT!)
  - **Branch:** `main`
  - **Root Directory:** (leave blank)
  - **Runtime:** Docker
  - **Instance Type:** 
    - Free (for testing, sleeps after 15 min)
    - Starter $7/mo (recommended for production)

- [ ] Click "Create Web Service"

### 2. Configure Environment Variables

In Render Web Service → Environment tab:

**Required Variables:**

- [ ] `FLASK_ENV` = `production`
- [ ] `SECRET_KEY` = (generate random 32+ char string)
- [ ] `DEBUG` = `False`
- [ ] `PORT` = `10000`
- [ ] `PYTHONUNBUFFERED` = `1`
- [ ] `DATABASE_URL` = (paste Internal Database URL from above)
- [ ] `AT_USERNAME` = `Kwepo`
- [ ] `AT_API_KEY` = (your AfricasTalking API key)
- [ ] `AT_SHORTCODE` = `20384`
- [ ] `AT_SENDER_ID` = `AFTKNG`
- [ ] `CONDUCTOR_USERNAME` = `admin`
- [ ] `CONDUCTOR_PASSWORD` = (strong password, NOT admin123!)

**Verification:**

- [ ] Click "Save Changes"
- [ ] Wait for automatic redeployment (~3-5 minutes)

### 3. Wait for First Deployment

- [ ] Watch build logs (Logs tab)
- [ ] Wait for "Build successful" message
- [ ] Wait for "Deploy successful" message
- [ ] Check status shows "Live"

### 4. Get Your App URL

- [ ] Copy URL from dashboard:
  ```
  https://nazigi-stamford-sms.onrender.com
  ```

- [ ] Save to secure location

---

## 🗃️ Database Migration on Render

### 1. Access Render Shell

- [ ] Go to Web Service dashboard
- [ ] Click "Shell" tab (top right)
- [ ] Wait for shell to connect

### 2. Run Migrations

- [ ] Execute in shell:
  ```bash
  flask db upgrade
  ```
  OR
  ```bash
  python init_db.py
  ```

- [ ] Verify success (should see "Migration complete" or similar)

### 3. Verify Database

- [ ] Check tables created:
  ```bash
  python -c "
  from app import create_app, db
  from models import Passenger, ConductorMessage, PassengerResponse, SMSLog
  app = create_app()
  with app.app_context():
      print(f'Passengers: {Passenger.query.count()}')
      print(f'Messages: {ConductorMessage.query.count()}')
      print('Tables created successfully!')
  "
  ```

---

## 📱 AfricasTalking Configuration

### 1. Update Callback URL

- [ ] Log into AfricasTalking: https://account.africastalking.com/
- [ ] Navigate to: SMS → Settings → Callback URLs
- [ ] Set "Incoming Messages Callback URL":
  ```
  https://nazigi-stamford-sms.onrender.com/sms/callback
  ```
- [ ] HTTP Method: POST
- [ ] Click "Save"

### 2. Verify Keyword Configuration

- [ ] Navigate to: SMS → Keywords
- [ ] Check keyword "TEST2" exists
- [ ] Mapped to shortcode "20384"
- [ ] Callback URL: Same as above
- [ ] Click "Save" if changed

### 3. Check Account Balance

- [ ] Dashboard → Account Balance
- [ ] Ensure sufficient balance (at least KES 50)
- [ ] Top up if needed

---

## 🧪 Production Testing

### 1. Basic Health Check

- [ ] Test home page:
  ```bash
  curl https://nazigi-stamford-sms.onrender.com/
  ```
  Should return HTML with "Nazigi Stamford"

- [ ] Test callback endpoint:
  ```bash
  curl -X POST https://nazigi-stamford-sms.onrender.com/sms/callback \
    -d "from=+254799489045" \
    -d "text=TEST2" \
    -d "to=20384"
  ```
  Should return: `{"status":"success","message":"Processed"}`

### 2. Dashboard Access

- [ ] Open in browser: https://nazigi-stamford-sms.onrender.com/conductor/dashboard
- [ ] Login with your credentials
- [ ] Verify dashboard loads with:
  - [ ] Total passengers count
  - [ ] Messages sent count
  - [ ] Recent activity
  - [ ] Send message form

### 3. Live SMS Testing

**Passenger Registration:**

- [ ] From your phone, send: `TEXT2` to `20384`
- [ ] Should receive welcome message within 30 seconds
- [ ] Reply: `1`
- [ ] Should receive opt-in confirmation

**Verify in Dashboard:**

- [ ] Refresh conductor dashboard
- [ ] Check "Total Passengers" increased by 1
- [ ] Click "View Passengers"
- [ ] Your phone number should appear in list

**Send Bulk Message:**

- [ ] In dashboard, enter test message:
  ```
  Test message - Bus leaving CBD now
  ```
- [ ] Click "Send Message"
- [ ] Should see success notification
- [ ] Your phone should receive message with stop list
- [ ] Reply: `5` (for Zimmerman)
- [ ] Should receive confirmation

**Verify Response:**

- [ ] In dashboard, click "View All Responses"
- [ ] Your response should appear with:
  - Your phone number
  - Selected stop: Zimmerman
  - Timestamp

### 4. Check Render Logs

- [ ] Go to Render → Web Service → Logs
- [ ] Verify logs show:
  ```
  📥 ========== INCOMING SMS ==========
  📱 From: +254799489045
  💬 Text: TEST2
  ```
- [ ] No error messages
- [ ] Status Code 200 for requests

---

## 🔧 Post-Deployment Configuration

### 1. Enable Auto-Deploy

- [ ] Go to Render → Web Service → Settings
- [ ] Under "Build & Deploy":
  - [ ] Auto-Deploy: **Yes**
  - [ ] Branch: `main`
- [ ] Click "Save Changes"

**Now every git push will auto-deploy!**

### 2. Configure Health Checks

- [ ] Go to Settings → Health Check
- [ ] Set "Health Check Path": `/`
- [ ] Click "Save"

**Render will restart your app if health check fails**

### 3. Set Up Notifications (Optional)

- [ ] Go to Settings → Notifications
- [ ] Add email for:
  - [ ] Deploy failures
  - [ ] Service downtimes
  - [ ] Health check failures

### 4. Custom Domain (Optional)

- [ ] Go to Settings → Custom Domain
- [ ] Add your domain (e.g., sms.nazigibus.com)
- [ ] Update DNS records as instructed
- [ ] Wait for SSL certificate provisioning

---

## 📊 Monitoring Setup

### Daily Checks

- [ ] Check Render dashboard for errors
- [ ] Monitor service uptime (Render shows this)
- [ ] Check AfricasTalking SMS logs
- [ ] Verify passenger growth in dashboard

### Weekly Checks

- [ ] Review Render logs for patterns
- [ ] Check database size (Render shows usage)
- [ ] Verify AfricasTalking balance
- [ ] Check response rates in dashboard

### Monthly Maintenance

- [ ] Rotate API keys (optional but recommended)
- [ ] Review and optimize database queries
- [ ] Update dependencies if needed
- [ ] Backup important data (Render does auto-backups)

---

## 🔒 Security Checklist

### Production Security

- [ ] `SECRET_KEY` is random, not default
- [ ] `CONDUCTOR_PASSWORD` is strong, not admin123
- [ ] `.env` file NOT in Git repository
- [ ] HTTPS enabled (automatic on Render)
- [ ] Database password is strong
- [ ] API keys stored in Render environment only

### Best Practices

- [ ] Environment variables in Render, not code
- [ ] Logs don't expose sensitive data
- [ ] Database uses Internal URL (free bandwidth)
- [ ] Regular password rotation schedule set
- [ ] Two-factor auth on Render account enabled

---

## ✅ Final Verification

**Complete this final test to ensure everything works:**

### 1. Send SMS Registration

- [ ] Phone: Send `TEXT2` to `20384`
- [ ] Receive: Welcome message
- [ ] Reply: `1`
- [ ] Receive: Opt-in confirmation

### 2. Conductor Operations

- [ ] Login: https://nazigi-stamford-sms.onrender.com/conductor/dashboard
- [ ] Send: Test bulk message
- [ ] Receive: SMS on phone with stop list
- [ ] Reply: `5` (any stop number)
- [ ] Receive: Confirmation SMS

### 3. Dashboard Analytics

- [ ] View: Passenger count updated
- [ ] View: Message history shows sent message
- [ ] View: Response analytics show your selection
- [ ] View: Charts/stats populate correctly

### 4. Error Handling

- [ ] Send: Invalid command (e.g., "HELLO")
- [ ] Receive: Helpful error message
- [ ] Check: Logs show proper error handling

### 5. Performance

- [ ] Dashboard loads in < 3 seconds
- [ ] SMS received in < 30 seconds
- [ ] No timeout errors in Render logs

---

## 🎉 Deployment Complete!

### You Did It! Your application is now:

✅ Dockerized for consistent environments  
✅ Deployed to Render for production hosting  
✅ Connected to PostgreSQL database  
✅ Integrated with AfricasTalking SMS gateway  
✅ Monitored with health checks  
✅ Secured with environment variables  
✅ Auto-deploying from GitHub  

### Your URLs:

- **Production App:** https://nazigi-stamford-sms.onrender.com
- **Dashboard:** https://nazigi-stamford-sms.onrender.com/conductor/dashboard
- **SMS Callback:** https://nazigi-stamford-sms.onrender.com/sms/callback
- **Render Dashboard:** https://dashboard.render.com/

### Credentials:

- **Dashboard:** (your `CONDUCTOR_USERNAME` / `CONDUCTOR_PASSWORD`)
- **Database:** (saved from Render PostgreSQL setup)
- **AfricasTalking:** (your API key and shortcode)

---

## 📚 Reference Documents

- **RENDER_DEPLOYMENT.md** - Full Render deployment guide
- **LOCAL_DOCKER_GUIDE.md** - Local Docker development
- **DOCKER_SUMMARY.md** - Quick command reference
- **README.md** - Complete application documentation

---

## 🆘 Need Help?

**Common Issues:**

1. **SMS not received:**
   - Check AfricasTalking callback URL is correct
   - Verify account balance
   - Check Render logs for incoming SMS

2. **Database connection failed:**
   - Verify DATABASE_URL format
   - Check database is running in Render
   - Ensure using Internal URL, not External

3. **App won't start:**
   - Check environment variables are set
   - Review Render build logs
   - Verify Dockerfile syntax

4. **Slow performance:**
   - Upgrade from Free to Starter plan
   - Check database is in same region as app
   - Review Gunicorn worker configuration

**Still stuck?**
- Check Render logs first
- Review AfricasTalking SMS logs
- Re-run this checklist step-by-step

---

**Congratulations! Your Nazigi Stamford Bus SMS Service is live! 🚀🚌📱**

Happy deploying! 🎊

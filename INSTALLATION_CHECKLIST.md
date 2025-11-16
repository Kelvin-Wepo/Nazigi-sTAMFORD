# 🚀 Nazigi SMS Service - Installation Checklist

## Pre-Installation Requirements

### System Requirements
- [ ] Ubuntu/Debian Linux server (20.04 LTS or newer recommended)
- [ ] Python 3.8 or higher installed
- [ ] PostgreSQL 12 or higher installed
- [ ] At least 1GB RAM
- [ ] 10GB disk space
- [ ] Public IP address or domain name

### Accounts Required
- [ ] AfricasTalking account created
- [ ] AfricasTalking API credentials obtained
- [ ] SMS shortcode (2045) configured
- [ ] Domain name (optional but recommended)

---

## Phase 1: System Preparation

### 1.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```
- [ ] System updated

### 1.2 Install Dependencies
```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```
- [ ] Python 3 installed
- [ ] PostgreSQL installed
- [ ] Nginx installed (for production)

### 1.3 Verify Installations
```bash
python3 --version  # Should be 3.8+
psql --version     # Should be 12+
nginx -v
```
- [ ] All versions verified

---

## Phase 2: Database Setup

### 2.1 Create Database User
```bash
sudo -u postgres psql
```

In PostgreSQL prompt:
```sql
CREATE DATABASE nazigi_sms;
CREATE USER nazigi_user WITH PASSWORD 'your_secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE nazigi_sms TO nazigi_user;
\q
```
- [ ] Database created
- [ ] User created
- [ ] Privileges granted

### 2.2 Test Database Connection
```bash
psql -h localhost -U nazigi_user -d nazigi_sms -c "SELECT version();"
```
- [ ] Can connect to database

---

## Phase 3: Application Setup

### 3.1 Clone/Download Project
```bash
cd /home/subchief
# Files should be in /home/subchief/Nazigi
```
- [ ] Project files in place

### 3.2 Run Setup Script
```bash
cd /home/subchief/Nazigi
chmod +x setup.sh
./setup.sh
```
- [ ] Virtual environment created
- [ ] Dependencies installed

### 3.3 Configure Environment
```bash
cp .env.example .env
nano .env
```

Update these values:
```env
AT_USERNAME=your_africastalking_username
AT_API_KEY=your_africastalking_api_key
AT_SHORTCODE=2045

DATABASE_URL=postgresql://nazigi_user:your_secure_password_here@localhost:5432/nazigi_sms

SECRET_KEY=generate_random_key_here
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=create_strong_password_here
```

- [ ] AfricasTalking credentials added
- [ ] Database URL configured
- [ ] Strong SECRET_KEY generated
- [ ] Conductor credentials set

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3.4 Initialize Database
```bash
source venv/bin/activate
python init_db.py
```
- [ ] Database tables created
- [ ] No errors during initialization

### 3.5 Test Application
```bash
python app.py
```

In another terminal:
```bash
curl http://localhost:5000/health
```
Should return: `{"status":"healthy"}`

- [ ] Application starts without errors
- [ ] Health endpoint responds

Press Ctrl+C to stop the test server.

---

## Phase 4: AfricasTalking Configuration

### 4.1 Login to AfricasTalking Dashboard
- [ ] Logged in to africastalking.com

### 4.2 Configure Shortcode
- [ ] Shortcode 2045 is active
- [ ] Shortcode is assigned to your account

### 4.3 Set SMS Callback URL

**Development (for testing):**
Use ngrok or similar:
```bash
ngrok http 5000
```
Callback URL: `https://your-ngrok-url.ngrok.io/sms/callback`

**Production:**
Callback URL: `https://your-domain.com/sms/callback`

Steps:
1. Go to SMS → Settings in AT Dashboard
2. Set Callback URL
3. Select POST method
4. Save

- [ ] Callback URL configured
- [ ] POST method selected
- [ ] Changes saved

### 4.4 Test SMS (Sandbox Mode)
- [ ] Added test phone number in AT dashboard
- [ ] Sent test SMS
- [ ] Received SMS successfully

---

## Phase 5: Production Deployment

### 5.1 Install Gunicorn
```bash
source venv/bin/activate
pip install gunicorn
```
- [ ] Gunicorn installed

### 5.2 Create Systemd Service
```bash
sudo nano /etc/systemd/system/nazigi-sms.service
```

Paste:
```ini
[Unit]
Description=Nazigi Stamford Bus SMS Service
After=network.target postgresql.service

[Service]
Type=simple
User=subchief
WorkingDirectory=/home/subchief/Nazigi
Environment="PATH=/home/subchief/Nazigi/venv/bin"
ExecStart=/home/subchief/Nazigi/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

- [ ] Service file created

### 5.3 Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable nazigi-sms
sudo systemctl start nazigi-sms
sudo systemctl status nazigi-sms
```
- [ ] Service enabled
- [ ] Service started
- [ ] Service status shows "active (running)"

### 5.4 Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/nazigi-sms
```

Paste:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Change this!

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

- [ ] Nginx config created
- [ ] Domain name updated

### 5.5 Enable Nginx Site
```bash
sudo ln -s /etc/nginx/sites-available/nazigi-sms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
- [ ] Site enabled
- [ ] Nginx config valid
- [ ] Nginx restarted

### 5.6 Configure Firewall
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
sudo ufw status
```
- [ ] Firewall configured
- [ ] Ports 80, 443 open

### 5.7 Install SSL Certificate
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Follow prompts and select option 2 (redirect HTTP to HTTPS)

- [ ] SSL certificate installed
- [ ] Auto-renewal configured
- [ ] HTTPS working

### 5.8 Update AfricasTalking Callback
- [ ] Updated callback URL to: `https://your-domain.com/sms/callback`
- [ ] Verified with HTTPS (not HTTP)

---

## Phase 6: Testing

### 6.1 Test Web Interface
1. Open browser: `https://your-domain.com`
2. Login with conductor credentials
3. View dashboard

- [ ] Web interface loads
- [ ] Can login
- [ ] Dashboard shows correct data

### 6.2 Test Passenger Flow

**Test 1: Opt-In**
```
Send SMS: "stamford" to 2045
Expected: Welcome message with opt-in options
```
- [ ] Received welcome message

**Test 2: Confirm Opt-In**
```
Send SMS: "YES" to 2045
Expected: Confirmation message
```
- [ ] Received confirmation

**Test 3: Conductor Message**
```
1. Login to web dashboard
2. Type message: "Test message"
3. Click Send
Expected: Receive SMS with stop list
```
- [ ] Conductor can send message
- [ ] Passenger receives message with stops

**Test 4: Stop Selection**
```
Send SMS: "5" to 2045
Expected: Confirmation of stop selection
```
- [ ] Received stop confirmation
- [ ] Response logged in dashboard

**Test 5: Opt-Out**
```
Send SMS: "STOP" to 2045
Expected: Opt-out confirmation
```
- [ ] Received opt-out confirmation
- [ ] No longer receives messages

### 6.3 Test API Endpoints
```bash
# Test health
curl https://your-domain.com/health

# Test dashboard (replace credentials)
curl -u admin:password https://your-domain.com/conductor/dashboard

# Test send message
curl -X POST https://your-domain.com/conductor/send-message \
  -u admin:password \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

- [ ] All API endpoints respond correctly

---

## Phase 7: Monitoring & Maintenance

### 7.1 Setup Log Monitoring
```bash
# View logs
sudo journalctl -u nazigi-sms -f
```
- [ ] Can view application logs

### 7.2 Database Backup Script
```bash
nano ~/backup-nazigi.sh
```

Paste:
```bash
#!/bin/bash
BACKUP_DIR="/home/subchief/backups"
mkdir -p $BACKUP_DIR
pg_dump nazigi_sms > $BACKUP_DIR/nazigi_$(date +%Y%m%d_%H%M%S).sql
# Keep only last 7 days
find $BACKUP_DIR -name "nazigi_*.sql" -mtime +7 -delete
```

Make executable:
```bash
chmod +x ~/backup-nazigi.sh
```

Setup cron:
```bash
crontab -e
```

Add:
```
0 2 * * * /home/subchief/backup-nazigi.sh
```

- [ ] Backup script created
- [ ] Cron job scheduled

### 7.3 Monitor Disk Space
```bash
df -h
du -sh /home/subchief/Nazigi
```
- [ ] Adequate disk space available

### 7.4 Check Service Status
```bash
sudo systemctl status nazigi-sms postgresql nginx
```
- [ ] All services running

---

## Phase 8: Documentation & Training

### 8.1 Conductor Training
- [ ] Conductors trained on web interface
- [ ] Know how to login
- [ ] Know how to send messages
- [ ] Know how to view responses

### 8.2 Passenger Onboarding
- [ ] Printed materials prepared
- [ ] In-bus announcements ready
- [ ] Posters with instructions displayed

### 8.3 Support Documentation
- [ ] README.md reviewed
- [ ] QUICKSTART.md available
- [ ] Support contact information distributed

---

## Phase 9: Go Live

### 9.1 Pre-Launch Checks
- [ ] All tests passed
- [ ] AfricasTalking account funded
- [ ] Callback URL verified
- [ ] SSL certificate valid
- [ ] Backup system working
- [ ] Monitoring in place

### 9.2 Soft Launch
- [ ] Start with small group (10-20 passengers)
- [ ] Monitor for 24 hours
- [ ] Fix any issues
- [ ] Verify all flows work

### 9.3 Full Launch
- [ ] Announce to all passengers
- [ ] Monitor closely for first week
- [ ] Collect feedback
- [ ] Make adjustments as needed

---

## Verification Commands

Run these to verify everything is working:

```bash
# 1. Check service status
sudo systemctl status nazigi-sms postgresql nginx

# 2. Check if app is responding
curl -s https://your-domain.com/health | jq

# 3. Check database connection
psql -h localhost -U nazigi_user -d nazigi_sms -c "SELECT COUNT(*) FROM passengers;"

# 4. Check logs (last 10 lines)
sudo journalctl -u nazigi-sms -n 10 --no-pager

# 5. Check SSL certificate
sudo certbot certificates

# 6. Test conductor login
curl -u admin:password https://your-domain.com/conductor/dashboard | jq

# 7. Check disk space
df -h | grep -E '/$|/home'

# 8. Check process
ps aux | grep gunicorn
```

All should return expected results with no errors.

---

## Troubleshooting Quick Reference

| Issue | Check | Solution |
|-------|-------|----------|
| App won't start | Service logs | `sudo journalctl -u nazigi-sms -n 50` |
| SMS not received | AT callback URL | Verify in AT dashboard |
| Can't connect to DB | PostgreSQL running | `sudo systemctl status postgresql` |
| Web interface 502 | Gunicorn running | `sudo systemctl restart nazigi-sms` |
| SSL not working | Certificate status | `sudo certbot renew --dry-run` |
| Login failed | Credentials | Check `.env` file |

---

## Post-Installation

### Regular Maintenance Tasks

**Daily:**
- [ ] Check service status
- [ ] Review error logs

**Weekly:**
- [ ] Review SMS logs
- [ ] Check passenger count
- [ ] Monitor response rates
- [ ] Verify backups

**Monthly:**
- [ ] Update system packages
- [ ] Review and optimize database
- [ ] Check disk space
- [ ] Review AfricasTalking billing

---

## Success Criteria

Your installation is complete when:

✅ Application is running as systemd service  
✅ Web interface accessible via HTTPS  
✅ Passengers can opt-in via SMS  
✅ Conductors can send messages  
✅ Passengers can select stops  
✅ Responses visible in dashboard  
✅ All logs recording properly  
✅ Backups running automatically  
✅ SSL certificate auto-renewing  
✅ AfricasTalking webhook working  

---

## Support Contacts

**Application Logs:**
```bash
sudo journalctl -u nazigi-sms -f
```

**Database Issues:**
```bash
sudo -u postgres psql nazigi_sms
```

**AfricasTalking Support:**
- Dashboard: https://account.africastalking.com
- Support: support@africastalking.com

---

**Installation Date:** _______________  
**Installed By:** _______________  
**Production URL:** _______________  
**Version:** 1.0.0

---

🎉 **Congratulations! Your Nazigi SMS Service is ready for production!** 🚀

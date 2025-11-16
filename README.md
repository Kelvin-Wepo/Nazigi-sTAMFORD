# 🚌 Nazigi Stamford Bus SMS Service

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![AfricasTalking](https://img.shields.io/badge/AfricasTalking-SMS-orange.svg)](https://africastalking.com/)

> **A production-ready, bi-directional bulk SMS service** enabling seamless communication between Nazigi Stamford Bus conductors and passengers. Built with Flask, PostgreSQL, and AfricasTalking API.

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Deployment](#deployment)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Monitoring & Logging](#monitoring--logging)

---

## 🎯 Overview

Nazigi Stamford Bus SMS Service streamlines passenger pickup by allowing conductors to broadcast location updates and collect passenger pickup preferences via SMS. The system features:

- **Two-way communication** between conductors and passengers
- **Automated opt-in/opt-out** workflow with compliance
- **10 designated bus stops** along the Nairobi-Kahawa West route
- **Real-time response tracking** with comprehensive analytics
- **Web dashboard** for conductor operations
- **Enterprise-grade logging** for debugging and monitoring

### Why This System?

- ✅ **No App Required** - Works with basic SMS on any phone
- ✅ **Real-time Updates** - Passengers get instant notifications
- ✅ **Organized Pickups** - Conductors know exactly where to stop
- ✅ **Cost-effective** - SMS at ~KES 0.80 per message
- ✅ **Scalable** - Handles hundreds of passengers efficiently

---

## ✨ Key Features

### 👥 Passenger Features

| Feature | Description | SMS Command |
|---------|-------------|-------------|
| **Opt-in** | Register for bus updates | Send `STAMFORD` to `3854` |
| **Opt-out** | Unsubscribe from service | Send `STOP` or `NO` |
| **Stop Selection** | Choose pickup location | Reply with `1-10` or stop name |
| **Smart Parsing** | Flexible input recognition | `5`, `Zimmerman`, `zimmer` all work |

**Available Bus Stops:**
1. 🚏 Ngara
2. 🚏 Allsops
3. 🚏 Homeland
4. 🚏 TRM
5. 🚏 Zimmerman
6. 🚏 Githurai 44
7. 🚏 Maziwa
8. 🚏 Kijito
9. 🚏 Kamiti
10. 🚏 Kahawa West Rounda

### 🎛️ Conductor Features (Admin)

| Feature | Access Method |
|---------|---------------|
| **Bulk Messaging** | Send updates to all opted-in passengers with stop selection menu |
| **Custom Messages** | Broadcast announcements without stop prompts |
| **Passenger List** | View all registered passengers and opt-in status |
| **Response Tracking** | See which passengers selected which stops |
| **Message History** | Access all sent messages with timestamps and recipient counts |
| **Analytics Dashboard** | Real-time statistics and engagement metrics |
| **Web Interface** | User-friendly HTML dashboard with authentication |

---

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Web Framework** | Flask | 3.0.0 |
| **Database** | PostgreSQL | 12+ |
| **SMS Gateway** | AfricasTalking | Latest |
| **ORM** | SQLAlchemy | Latest |
| **Migrations** | Flask-Migrate | Latest |
| **HTTP Server** | Gunicorn | 21.2.0 |
| **Environment** | Python | 3.8+ |

### 📁 Project Structure

```
Nazigi/
├── 📄 app.py                      # Main Flask application entry point
├── ⚙️  config.py                   # Configuration & environment settings
├── 🗄️  models.py                   # SQLAlchemy database models
├── 📱 sms_service.py              # AfricasTalking SMS integration
├── 🔧 init_db.py                  # Database initialization script
├── 📋 requirements.txt            # Python dependencies
├── 🔐 .env                        # Environment variables (not in git)
├── 📖 README.md                   # This documentation
├── 🚀 START_HERE.txt              # Quick start guide
│
├── routes/                        # Flask blueprints
│   ├── 📨 sms_routes.py           # SMS callback handlers (passenger interactions)
│   ├── 👨‍✈️ conductor_routes.py      # Admin API endpoints
│   └── __init__.py                # Routes package initializer
│
├── templates/                     # HTML templates
│   └── 🖥️  conductor.html          # Admin web dashboard
│
├── migrations/                    # Database migrations (Flask-Migrate)
│   ├── versions/                  # Migration scripts
│   └── alembic.ini               # Alembic configuration
│
├── venv/                          # Virtual environment (not in git)
└── logs/                          # Application logs (optional)
```

### 🔄 System Flow

```
┌─────────────────┐
│   Passenger     │
│  (SMS: 3854)    │
└────────┬────────┘
         │ 1. Sends "STAMFORD"
         ▼
┌─────────────────────────────┐
│   AfricasTalking Gateway    │
└────────┬────────────────────┘
         │ 2. POST to /sms/callback
         ▼
┌─────────────────────────────┐
│    Flask Application        │
│  - Routes incoming SMS      │
│  - Processes commands       │
│  - Sends responses          │
└────────┬────────────────────┘
         │ 3. Stores in DB
         ▼
┌─────────────────────────────┐
│    PostgreSQL Database      │
│  - Passengers               │
│  - Messages                 │
│  - Responses                │
│  - Logs                     │
└────────┬────────────────────┘
         │ 4. Analytics
         ▼
┌─────────────────────────────┐
│   Conductor Dashboard       │
│  - View stats               │
│  - Send messages            │
│  - Track responses          │
└─────────────────────────────┘
```

---

## 🚀 Quick Start

**Prerequisites:** Python 3.8+, PostgreSQL 12+, AfricasTalking account

```bash
# 1. Clone repository
cd /home/subchief/Nazigi

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add your credentials

# 5. Initialize database
python init_db.py

# 6. Run application
python app.py
```

Application will be running at `http://localhost:5000`

---

## 📦 Installation

### Prerequisites

Ensure you have the following installed:

- ✅ **Python 3.8+** - [Download](https://www.python.org/downloads/)
- ✅ **PostgreSQL 12+** - [Installation Guide](https://www.postgresql.org/download/)
- ✅ **pip** - Python package manager (comes with Python)
- ✅ **Git** - Version control (optional)
- ✅ **AfricasTalking Account** - [Sign up](https://africastalking.com/)

### Step-by-Step Installation

#### 1️⃣ Set Up Virtual Environment

```bash
cd /home/subchief/Nazigi

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

#### 2️⃣ Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Core dependencies installed:**
- Flask 3.0.0 - Web framework
- psycopg2-binary - PostgreSQL adapter
- SQLAlchemy - ORM
- Flask-Migrate - Database migrations
- africastalking - SMS API client
- python-dotenv - Environment variable management
- gunicorn - Production WSGI server

#### 3️⃣ Configure PostgreSQL Database

```bash
# Access PostgreSQL as superuser
sudo -u postgres psql

# Create database and user
CREATE DATABASE nazigi_sms;
CREATE USER nazigi_user WITH PASSWORD 'nazigi2025';
GRANT ALL PRIVILEGES ON DATABASE nazigi_sms TO nazigi_user;

# Grant schema privileges (PostgreSQL 15+)
\c nazigi_sms
GRANT ALL ON SCHEMA public TO nazigi_user;

# Exit PostgreSQL
\q
```

**Database Specifications:**
- **Database Name:** `nazigi_sms`
- **User:** `nazigi_user`
- **Password:** `nazigi2025` (change in production!)
- **Host:** `localhost`
- **Port:** `5432`

#### 4️⃣ Configure Environment Variables

Create `.env` file in project root:

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required Environment Variables:**

```env
# AfricasTalking Configuration
AT_USERNAME=""               # Your AT username (or "sandbox" for testing)
AT_API_KEY=""
AT_SHORTCODE=""               # Your shortcode (sandbox or production)
AT_SENDER_ID= ""            # Sender ID for branding

# Database Configuration
DATABASE_URL=postgresql://nazigi_user:nazigi2025@localhost:5432/nazigi_sms

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-in-production-12345
FLASK_ENV=development            # Use 'production' for deployment
DEBUG=True                       # Set to False in production

# Conductor Authentication
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=admin123      # CHANGE THIS IN PRODUCTION!

# Server Configuration
PORT=5000
```

⚠️ **Security Notes:**
- Never commit `.env` to version control (already in `.gitignore`)
- Use strong passwords for production
- Rotate API keys regularly
- Use environment-specific configurations

#### 5️⃣ Initialize Database

```bash
# Run initialization script
python init_db.py
```

**This script will:**
- ✅ Create all database tables (Passengers, ConductorMessages, PassengerResponses, SMSLogs)
- ✅ Set up proper relationships and constraints
- ✅ Create indexes for performance
- ✅ Verify database connectivity

**Expected Output:**
```
Database initialized successfully!
Tables created: passengers, conductor_messages, passenger_responses, sms_logs
```

#### 6️⃣ Run the Application

**Development Mode:**
```bash
python app.py
```

**Production Mode (with Gunicorn):**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Application will be accessible at:
- **Local:** http://localhost:5000
- **Network:** http://YOUR_IP:5000
- **Dashboard:** http://localhost:5000/conductor/dashboard

---

## ⚙️ Configuration

### AfricasTalking Setup

#### 1. Create AfricasTalking Account

1. Visit [africastalking.com](https://africastalking.com)
2. Sign up for an account
3. Verify your email and phone number

#### 2. Get API Credentials

**Sandbox (Testing):**
```
Username: sandbox
API Key: [Get from Dashboard → Settings → API Key]
Shortcode: Provided by AT (e.g., 3854)
```

**Production:**
```
Username: Your chosen username (e.g., "test")
API Key: [Get from Dashboard → Settings → API Key]
Shortcode: Your purchased shortcode
```

#### 3. Configure Callback URL

**Critical Step:** Tell AfricasTalking where to send incoming SMS

1. Log into AfricasTalking Dashboard
2. Navigate to: **SMS → Settings → Callback URLs**
3. Set **Incoming Messages URL** to:
   ```
   https://your-domain.com/sms/callback
   ```
   - Use your actual domain or ngrok URL for testing
   - Must be publicly accessible (HTTPS recommended)
   - Method: **POST**

**For Local Development (using ngrok):**
```bash
# Install ngrok
brew install ngrok  # Mac
# OR download from https://ngrok.com

# Start ngrok tunnel
ngrok http 5000

# Copy HTTPS URL (e.g., https://abc123.ngrok.io)
# Set in AfricasTalking: https://abc123.ngrok.io/sms/callback
```

#### 4. Test Configuration

```bash
# Send test SMS
python test_sms_send.py
```

### Database Configuration

**Connection String Format:**
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

**Example configurations:**

```env
# Local development
DATABASE_URL=postgresql://nazigi_user:nazigi2025@localhost:5432/nazigi_sms

# Remote database
DATABASE_URL=postgresql://user:pass@db.example.com:5432/nazigi_sms

# Docker container
DATABASE_URL=postgresql://user:pass@postgres:5432/nazigi_sms
```

### Conductor Authentication

The system uses **HTTP Basic Authentication** for conductor endpoints.

**Configure in `.env`:**
```env
CONDUCTOR_USERNAME=admin
CONDUCTOR_PASSWORD=your_secure_password_here
```

**Using in requests:**
```bash
# cURL example
curl -u admin:password http://localhost:5000/conductor/dashboard

# Python requests example
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    'http://localhost:5000/conductor/passengers',
    auth=HTTPBasicAuth('admin', 'password')
)
```

---

## 📱 Usage

### Passenger Workflow

#### Step 1: Opt-In to Service

**Action:** Send `STAMFORD` to shortcode `3854`

**System Response:**
```
Welcome to Nazigi Stamford Bus Service! 🚌

Would you like to receive updates about bus locations and pickup points?

Reply:
1 or YES to Opt In
2 or NO to Opt Out
```

#### Step 2: Confirm Opt-In

**Action:** Reply with `YES`, `Y`, `1`, or `OPT IN`

**System Response:**
```
Thank you for opting in! ✅

You will now receive updates from Nazigi Stamford Bus conductors.

To opt out anytime, send STOP to 3854.
```

#### Step 3: Receive Bus Updates

**When conductor sends message, you receive:**
```
Nazigi Stamford bus is now leaving CBD heading to Kahawa West. Where would you like to be picked?

Please reply with the number of your preferred stop:

1. Ngara
2. Allsops
3. Homeland
4. TRM
5. Zimmerman
6. Githurai 44
7. Maziwa
8. Kijito
9. Kamiti
10. Kahawa West Rounda

Reply with the number or name of your preferred stop.
```

#### Step 4: Select Pickup Stop

**Option A - By Number:**
Send: `5`

**Option B - By Name:**
Send: `Zimmerman` or `zimmer` or `ZIMMERMAN`

**System Response:**
```
✅ Confirmed! You will be picked up at Zimmerman.

Thank you for using Nazigi Stamford Bus Service!
```

#### Optional: Opt-Out

**Action:** Send `STOP`, `NO`, `2`, or `OPT OUT`

**System Response:**
```
You have been opted out from Nazigi Stamford Bus Service.

To opt in again, send STAMFORD to 3854.
```

---

### Conductor Operations

#### Access Dashboard

**Web Interface:**
```
URL: http://localhost:5000/conductor/dashboard
Username: admin
Password: admin123
```

**Features:**
- 📊 Real-time statistics (total passengers, opt-in rate, messages sent)
- 📨 Send bulk messages with stop selection
- 📝 Send custom announcements
- 👥 View all passengers
- 📋 View response analytics

#### Send Bulk Message (with Stop Selection)

**Via Web Dashboard:**
1. Log into dashboard
2. Enter message in "Send Message" section
3. Click "Send Message"
4. System automatically appends stop selection menu

**Via API (cURL):**
```bash
curl -X POST http://localhost:5000/conductor/send-message \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Nazigi Stamford bus is now leaving CBD heading to Kahawa West. Where would you like to be picked?"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Message sent to 25 passengers",
  "recipients_count": 25,
  "message_id": 15
}
```

#### Send Custom Message (without Stop Selection)

**Via API:**
```bash
curl -X POST http://localhost:5000/conductor/send-custom \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "⚠️ Service Alert: Bus delayed by 15 minutes due to traffic. Apologies for inconvenience."
  }'
```

#### View Passengers List

**Via API:**
```bash
curl -X GET http://localhost:5000/conductor/passengers \
  -u admin:admin123
```

**Response:**
```json
{
  "total": 47,
  "opted_in": 35,
  "opted_out": 12,
  "passengers": [
    {
      "id": 1,
      "phone_number": "+254711082300",
      "opted_in": true,
      "created_at": "2025-11-15T10:30:00"
    },
    ...
  ]
}
```

#### Track Responses by Message

**Via API:**
```bash
curl -X GET "http://localhost:5000/conductor/responses?message_id=15" \
  -u admin:admin123
```

**Response:**
```json
{
  "message_id": 15,
  "total_responses": 23,
  "responses_by_stop": {
    "Ngara": 2,
    "Allsops": 1,
    "Homeland": 3,
    "TRM": 4,
    "Zimmerman": 8,
    "Githurai 44": 3,
    "Maziwa": 1,
    "Kijito": 0,
    "Kamiti": 1,
    "Kahawa West Rounda": 0
  },
  "responses": [
    {
      "passenger_phone": "+254711082300",
      "selected_stop": "Zimmerman",
      "responded_at": "2025-11-17T14:25:30"
    },
    ...
  ]
}
```

#### View Message History

**Via API:**
```bash
curl -X GET http://localhost:5000/conductor/messages \
  -u admin:admin123
```

**Response:**
```json
{
  "total_messages": 28,
  "messages": [
    {
      "id": 15,
      "message_text": "Nazigi Stamford bus is now leaving...",
      "recipients_count": 25,
      "sent_at": "2025-11-17T14:20:00"
    },
    ...
  ]
}
```

---

## 📚 API Documentation

### Base URL

```
Development: http://localhost:5000
Production: https://your-domain.com
```

### Authentication

**Conductor endpoints** require HTTP Basic Authentication:
- **Username:** From `CONDUCTOR_USERNAME` in `.env`
- **Password:** From `CONDUCTOR_PASSWORD` in `.env`

**Passenger endpoints** are publicly accessible (called by AfricasTalking).

---

### Passenger Endpoints

#### 📥 SMS Callback Handler

**Endpoint:** `POST /sms/callback`

**Purpose:** Receives all incoming SMS from AfricasTalking

**Request (from AfricasTalking):**
```
Content-Type: application/x-www-form-urlencoded

from=+254711082300
text=STAMFORD
linkId=SampleLinkId123
date=2025-11-17 14:20:30
id=ATXid_sample123
to=3854
```

**Supported Commands:**

| Command | Aliases | Action |
|---------|---------|--------|
| `STAMFORD` | `stamford`, `Stamford` | Initiate opt-in process |
| `YES` | `yes`, `y`, `Y`, `1`, `opt in`, `optin` | Confirm opt-in |
| `NO` | `no`, `n`, `N`, `2`, `opt out`, `optout` | Opt-out from service |
| `STOP` | `stop`, `STOP` | Opt-out from service |
| `1-10` | Any digit 1-10 | Select stop by number |
| `Stop Name` | `Zimmerman`, `zimmer`, etc. | Select stop by name (fuzzy match) |

**Response:**
```json
{
  "status": "success",
  "message": "Processed"
}
```

**Error Response:**
```json
{
  "error": "Error message"
}
```

---

### Conductor Endpoints

All require `Authorization: Basic base64(username:password)`

#### 📤 Send Bulk Message with Stop Selection

**Endpoint:** `POST /conductor/send-message`

**Purpose:** Send message to all opted-in passengers with stop selection menu

**Request:**
```json
{
  "message": "Nazigi Stamford bus is now leaving CBD heading to Kahawa West. Where would you like to be picked?"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Message sent to 25 passengers",
  "recipients_count": 25,
  "message_id": 15,
  "africastalking_response": {
    "SMSMessageData": {
      "Message": "Sent to 25/25 Total Cost: KES 20.00",
      "Recipients": [...]
    }
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/conductor/send-message \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bus leaving CBD now heading to Kahawa West. Where would you like to be picked?"
  }'
```

---

#### 📢 Send Custom Message

**Endpoint:** `POST /conductor/send-custom`

**Purpose:** Send announcement without stop selection menu

**Request:**
```json
{
  "message": "⚠️ Service Alert: Bus delayed by 15 minutes due to traffic."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Custom message sent to 25 passengers",
  "recipients_count": 25
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/conductor/send-custom \
  -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Service will resume tomorrow at 6 AM. Thank you for your patience."
  }'
```

---

#### 👥 Get Passengers List

**Endpoint:** `GET /conductor/passengers`

**Purpose:** Retrieve all registered passengers with opt-in status

**Response:**
```json
{
  "total": 47,
  "opted_in": 35,
  "opted_out": 12,
  "passengers": [
    {
      "id": 1,
      "phone_number": "+254711082300",
      "opted_in": true,
      "created_at": "2025-11-15T10:30:00",
      "updated_at": "2025-11-17T14:20:00"
    },
    {
      "id": 2,
      "phone_number": "+254722123456",
      "opted_in": false,
      "created_at": "2025-11-16T09:15:00",
      "updated_at": "2025-11-16T09:20:00"
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/conductor/passengers \
  -u admin:admin123
```

---

#### 📊 Get Passenger Responses

**Endpoint:** `GET /conductor/responses?message_id={id}`

**Purpose:** View responses for a specific message or all recent responses

**Query Parameters:**
- `message_id` (optional): Filter by specific message ID

**Response (with message_id):**
```json
{
  "message_id": 15,
  "message_text": "Bus leaving CBD...",
  "total_responses": 23,
  "sent_to": 25,
  "response_rate": "92%",
  "responses_by_stop": {
    "Ngara": 2,
    "Allsops": 1,
    "Homeland": 3,
    "TRM": 4,
    "Zimmerman": 8,
    "Githurai 44": 3,
    "Maziwa": 1,
    "Kijito": 0,
    "Kamiti": 1,
    "Kahawa West Rounda": 0
  },
  "responses": [
    {
      "id": 45,
      "passenger_id": 12,
      "passenger_phone": "+254711082300",
      "response_text": "5",
      "selected_stop": "Zimmerman",
      "responded_at": "2025-11-17T14:25:30"
    }
  ]
}
```

**Response (without message_id - recent responses):**
```json
{
  "total_responses": 156,
  "recent_responses": [
    {
      "id": 156,
      "passenger_phone": "+254711082300",
      "message_text": "Bus leaving CBD...",
      "response_text": "5",
      "selected_stop": "Zimmerman",
      "responded_at": "2025-11-17T14:25:30"
    }
  ]
}
```

**cURL Example:**
```bash
# Get responses for specific message
curl -X GET "http://localhost:5000/conductor/responses?message_id=15" \
  -u admin:admin123

# Get all recent responses
curl -X GET http://localhost:5000/conductor/responses \
  -u admin:admin123
```

---

#### 📜 Get Message History

**Endpoint:** `GET /conductor/messages`

**Purpose:** Retrieve all messages sent by conductors

**Response:**
```json
{
  "total_messages": 28,
  "messages": [
    {
      "id": 28,
      "message_text": "Bus leaving CBD heading to Kahawa West...",
      "recipients_count": 25,
      "sent_at": "2025-11-17T14:20:00",
      "responses_count": 23
    },
    {
      "id": 27,
      "message_text": "Service delayed by 15 minutes...",
      "recipients_count": 25,
      "sent_at": "2025-11-17T08:45:00",
      "responses_count": 0
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:5000/conductor/messages \
  -u admin:admin123
```

---

#### 📈 Get Dashboard Statistics

**Endpoint:** `GET /conductor/dashboard`

**Purpose:** Retrieve real-time statistics and analytics

**Response (HTML):**
Returns rendered HTML dashboard with:
- Total passengers
- Opted-in count
- Opt-in percentage
- Total messages sent
- Recent activity
- Interactive controls

**cURL Example (API data):**
```bash
curl -X GET http://localhost:5000/conductor/dashboard \
  -u admin:admin123 \
  -H "Accept: application/json"
```

---

### Error Responses

**401 Unauthorized:**
```json
{
  "error": "Unauthorized",
  "message": "Invalid credentials"
}
```

**400 Bad Request:**
```json
{
  "error": "Missing required field: message"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error",
  "message": "Error details..."
}
```

---
## 🗄️ Database Schema

The system uses **PostgreSQL** with **SQLAlchemy ORM**. All tables use auto-incrementing IDs and timestamps.

### Entity Relationship Diagram

```
┌─────────────────────┐
│     Passengers      │
├─────────────────────┤
│ PK id              │───┐
│    phone_number    │   │
│    opted_in        │   │
│    created_at      │   │
│    updated_at      │   │
└─────────────────────┘   │
                          │
                          │ 1:N
                          │
                          ▼
┌─────────────────────────────────┐
│    PassengerResponses           │
├─────────────────────────────────┤
│ PK id                           │
│ FK passenger_id ────────────────┤
│ FK message_id (nullable)        │◄───┐
│    response_text                │    │
│    selected_stop                │    │
│    responded_at                 │    │
└─────────────────────────────────┘    │
                                       │ N:1
                                       │
┌──────────────────────────────────────┤
│     ConductorMessages                │
├──────────────────────────────────────┤
│ PK id                                │
│    message_text                      │
│    recipients_count                  │
│    sent_at                           │
└──────────────────────────────────────┘

┌─────────────────────┐
│      SMSLogs        │
├─────────────────────┤
│ PK id              │
│    phone_number    │
│    message         │
│    direction       │
│    status          │
│    created_at      │
└─────────────────────┘
```

### Table: `passengers`

Stores registered passengers and their opt-in status.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment passenger ID |
| `phone_number` | VARCHAR(20) | UNIQUE, NOT NULL | E.164 format (+254...) |
| `opted_in` | BOOLEAN | NOT NULL, DEFAULT FALSE | Consent status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Registration timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
- `idx_phone_number` on `phone_number` (for fast lookups)
- `idx_opted_in` on `opted_in` (for filtering)

**Example Data:**
```sql
id | phone_number   | opted_in | created_at          | updated_at
---+----------------+----------+---------------------+--------------------
1  | +254711082300  | true     | 2025-11-15 10:30:00 | 2025-11-17 14:20:00
2  | +254722123456  | false    | 2025-11-16 09:15:00 | 2025-11-16 09:20:00
```

---

### Table: `conductor_messages`

Stores all messages sent by conductors.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment message ID |
| `message_text` | TEXT | NOT NULL | Message content sent |
| `recipients_count` | INTEGER | NOT NULL | Number of recipients |
| `sent_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When message was sent |

**Indexes:**
- `idx_sent_at` on `sent_at` (for chronological queries)

**Example Data:**
```sql
id | message_text                          | recipients_count | sent_at
---+---------------------------------------+------------------+--------------------
15 | Bus leaving CBD heading to Kahawa... | 25               | 2025-11-17 14:20:00
16 | Service delayed by 15 minutes...     | 25               | 2025-11-17 08:45:00
```

---

### Table: `passenger_responses`

Stores passenger replies to conductor messages.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment response ID |
| `passenger_id` | INTEGER | FOREIGN KEY → passengers.id | Who responded |
| `message_id` | INTEGER | FOREIGN KEY → conductor_messages.id, NULLABLE | Which message (if applicable) |
| `response_text` | TEXT | NOT NULL | Raw SMS response |
| `selected_stop` | VARCHAR(100) | NULLABLE | Parsed stop name |
| `responded_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Response timestamp |

**Indexes:**
- `idx_passenger_id` on `passenger_id` (for passenger history)
- `idx_message_id` on `message_id` (for message analytics)
- `idx_selected_stop` on `selected_stop` (for stop analytics)

**Foreign Keys:**
- `passenger_id` REFERENCES `passengers(id)` ON DELETE CASCADE
- `message_id` REFERENCES `conductor_messages(id)` ON DELETE SET NULL

**Example Data:**
```sql
id | passenger_id | message_id | response_text | selected_stop | responded_at
---+--------------+------------+---------------+---------------+--------------------
45 | 1            | 15         | 5             | Zimmerman     | 2025-11-17 14:25:30
46 | 2            | 15         | Ngara         | Ngara         | 2025-11-17 14:26:15
```

---

### Table: `sms_logs`

Audit trail for all SMS activity (incoming and outgoing).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Auto-increment log ID |
| `phone_number` | VARCHAR(20) | NOT NULL | Sender or recipient |
| `message` | TEXT | NOT NULL | Full message content |
| `direction` | VARCHAR(10) | NOT NULL | `incoming` or `outgoing` |
| `status` | VARCHAR(50) | NOT NULL | `sent`, `received`, `failed: reason` |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Log timestamp |

**Indexes:**
- `idx_phone_number_logs` on `phone_number` (for filtering by user)
- `idx_direction` on `direction` (for filtering by type)
- `idx_created_at_logs` on `created_at` (for time-based queries)

**Example Data:**
```sql
id | phone_number  | message             | direction | status | created_at
---+---------------+---------------------+-----------+--------+--------------------
89 | +254711082300 | STAMFORD            | incoming  | received | 2025-11-17 14:19:55
90 | +254711082300 | Welcome to Nazigi...| outgoing  | sent   | 2025-11-17 14:20:00
```

---

### Database Migrations

Using **Flask-Migrate** (Alembic):

```bash
# Initialize migrations (already done)
flask db init

# Create new migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback last migration
flask db downgrade

# View migration history
flask db history
```

---

### Sample Queries

**Count opted-in passengers:**
```sql
SELECT COUNT(*) FROM passengers WHERE opted_in = true;
```

**Get responses for a message:**
```sql
SELECT p.phone_number, pr.selected_stop, pr.responded_at
FROM passenger_responses pr
JOIN passengers p ON pr.passenger_id = p.id
WHERE pr.message_id = 15
ORDER BY pr.responded_at DESC;
```

**Get response analytics by stop:**
```sql
SELECT selected_stop, COUNT(*) as count
FROM passenger_responses
WHERE message_id = 15 AND selected_stop IS NOT NULL
GROUP BY selected_stop
ORDER BY count DESC;
```

**Find passengers who haven't responded:**
```sql
SELECT p.phone_number
FROM passengers p
WHERE p.opted_in = true
AND p.id NOT IN (
    SELECT passenger_id 
    FROM passenger_responses 
    WHERE message_id = 15
);
```

---
# Nazigi-sTAMFORD

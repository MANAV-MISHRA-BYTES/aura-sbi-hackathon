<div align="center">

# 🤖 AURA
### Autonomous User-Centric Retail Agent
**SBI × AI Hackathon 2025**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.3-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

> *"What if your bank acted before you even knew you needed it to?"*

</div>

---

## The Problem

Most banking apps are **reactive** — you log in, check your balance, and leave. Meanwhile ₹15,000 of your salary sits idle in a checking account earning 2.7% while inflation runs at 5.5%. Nobody nudges you. Nobody acts for you.

## The Solution

Aura is an **Agentic AI banking assistant** that runs silently in the background. It analyses your spending patterns, detects idle surplus funds after expenses, and surfaces **personalised, one-click action nudges** — right when they matter.

No dashboards to navigate. No forms to fill. Just one tap.

---

## Demo Flow

```
Salary credited → Aura agent wakes up
                        │
              Scans 30 days of transactions
              Detects surplus > ₹10,000
                        │
                        ▼
         💬 Chat bubble appears on dashboard:
   "₹13,000 is idle. Park it in SBI Liquid Fund at 7% p.a.?"
                        │
              ┌──────────────────┐
              │  ✅ Yes, execute │   ↩ Not now
              └──────────────────┘
                        │
               Funds moved instantly
                    Confetti 🎉
```

---

## Features

| | Feature | What it does |
|---|---|---|
| 🧠 | **Background Agent** | Celery worker continuously analyses finances |
| 💬 | **Conversational Nudges** | AI-generated chat bubbles, not forms |
| ⚡ | **One-Click Execution** | Single tap moves funds — no extra steps |
| 📊 | **Live Balance Updates** | Cards refresh instantly after every action |
| 🔄 | **Auto-polling** | Frontend polls nudges every 5s, widget opens on its own |
| 🎉 | **Celebration Feedback** | Canvas confetti on successful transfer |
| ♿ | **WCAG AA** | ARIA labels, skip-nav, landmark roles, 4.5:1 contrast |
| 🐳 | **Docker Ready** | One command starts all 4 services |

---

## Architecture

```
┌────────────────────────────────────────────┐
│            Browser  (Vue 3 SPA)            │
│   Dashboard · AccountCards · AuraWidget    │
└──────────────────┬─────────────────────────┘
                   │  /api/* requests
                   ▼
┌────────────────────────────────────────────┐
│        Vite Dev Server  (port 5173)        │
│        proxies  /api/* → Flask :5000       │
└──────────────────┬─────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────┐
│        Flask REST API  (port 5000)         │
│  /dashboard  /nudges  /execute-nudge       │
│  /dismiss-nudge  /trigger-agent            │
└──────────┬─────────────────┬───────────────┘
           │                 │
           ▼                 ▼
┌──────────────────┐  ┌─────────────────────┐
│    SQLite DB     │  │   Redis  (port 6379) │
│  users           │  │   Celery broker      │
│  transactions    │  └──────────┬──────────┘
│  actionable_     │             │
│  nudges          │             ▼
└──────────────────┘  ┌─────────────────────┐
                       │   Celery Worker      │
                       │   analyze_financial_ │
                       │   health             │
                       └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue 3 (Composition API), Tailwind CSS v3, Vite, Axios, canvas-confetti |
| **Backend** | Python 3.12, Flask 3.0, SQLAlchemy 2.0, Flask-CORS |
| **Database** | SQLite (prototype) — swap to PostgreSQL for production |
| **Agent** | Celery 5.3 + Redis 7 (async task queue + broker) |
| **AI / Logic** | Deterministic rule-based engine — zero API cost, consistent demo output |
| **DevOps** | Docker Compose (4-service: redis · flask · celery · frontend) |

---

## Quick Start

### 🐳 Option A — Docker (one command)

```bash
git clone https://github.com/MANAV-MISHRA-BYTES/aura-sbi-hackathon.git
cd aura-sbi-hackathon
docker-compose up --build
```

Open **http://localhost:5173**

---

### 💻 Option B — Local Development

**Backend** (Terminal 1)
```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python run.py
# Flask API → http://localhost:5000
```

**Frontend** (Terminal 2)
```bash
cd frontend
npm install
npm run dev
# Vite → http://localhost:5173
```

> **No Redis / Celery?** No problem. The `/api/trigger-agent` endpoint automatically falls back to synchronous execution. The entire demo works without any extra services running.

---

## Running the Demo

Once the servers are up:

1. Open `http://localhost:5173`
2. View **Rajesh Kumar's** dashboard — ₹65,000 checking, ₹12,500 savings, 10 real transactions
3. Click **⚡ Analyse Now** in the purple Aura section
4. The 🤖 floating widget (bottom-right) pulses and **opens by itself** with a personalised nudge
5. Click **✅ Yes, execute this**
6. Balances update live · confetti fires 🎉

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health check |
| `GET` | `/api/dashboard` | User profile + last 10 transactions |
| `GET` | `/api/nudges` | All pending AI nudges |
| `POST` | `/api/trigger-agent` | Manually fire the analysis agent |
| `POST` | `/api/execute-nudge` | Accept nudge → deduct checking, add savings |
| `POST` | `/api/dismiss-nudge` | Dismiss a nudge |

---

## Agent Logic

```
IF  checking_balance > ₹50,000
AND salary credit detected in last 30 days
AND surplus (balance − monthly debits) > ₹10,000

THEN
  invest_amount = min(surplus × 65%, ₹15,000)
                  rounded to nearest ₹1,000
  → Write ActionableNudge to database
```

Fully deterministic. No external AI API calls. Same result every run — ideal for live demos.

---

## Database Schema

```
users
  id · name · checking_balance · savings_balance

transactions
  id · user_id · amount · type (credit|debit) · category · description · timestamp

actionable_nudges
  id · user_id · message · proposed_action · amount · status (pending|accepted|dismissed) · created_at
```

---

## Project Structure

```
aura-sbi-hackathon/
├── docker-compose.yml
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py                    Flask entry point
│   ├── worker.py                 Celery worker entry point
│   └── app/
│       ├── __init__.py           App factory + DB seed
│       ├── config.py             Environment configuration
│       ├── models.py             SQLAlchemy models
│       ├── routes.py             REST API routes
│       ├── tasks.py              analyze_financial_health task
│       └── celery_factory.py     Flask ↔ Celery context wiring
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js            Proxy /api → Flask
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── main.js
        ├── App.vue
        ├── style.css
        ├── api/index.js          Axios API layer
        ├── views/
        │   └── Dashboard.vue     Main view + state management
        └── components/
            ├── AccountCard.vue       Gradient balance cards
            ├── TransactionList.vue   Transaction feed
            ├── AuraWidget.vue        Floating AI nudge widget (FAB)
            ├── NudgeCard.vue         Chat bubble + action buttons
            └── ConfettiEffect.vue    canvas-confetti celebration
```

---

## Colour System

| Token | Hex | Role |
|---|---|---|
| SBI Deep Blue | `#003478` | Header, primary actions |
| SBI Sky Blue | `#0072BC` | Savings card, accents |
| Aura Violet | `#7C3AED` | AI widget, nudge CTAs |
| Aura Indigo | `#4F46E5` | Gradients |
| Success Green | `#10B981` | Credits, confirmations |

**Font:** Inter (Google Fonts) &nbsp;·&nbsp; **Accessibility:** WCAG AA

---

<div align="center">
Made with ☕ for the SBI × AI Hackathon 2025
</div>

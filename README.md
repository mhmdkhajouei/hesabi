# Hesabi 💰

**Hesabi** (حسابی — "accounting" in Persian) is a personal finance tracking web app that helps users record income and expenses, manage category-based budgets, and monitor real-time spending balances — accessible from any device including mobile.

This project was built as a hands-on learning exercise to practice clean backend architecture, RESTful API design, and full-stack development with Python, Flask, and vanilla JavaScript.

---

## What it does

- Track income and expense transactions with date, category, and notes
- Organize spending into custom categories
- Set a monthly budget goal for each category
- Calculate real-time balances:
  - Total income / total expenses / overall remaining balance
  - Spending and remaining balance per category
  - Visual progress bars showing budget consumption
- View transaction and category detail pages
- Add, edit, and delete transactions and categories
- Fully responsive — works on desktop and mobile (bottom nav bar on small screens)

---

## Architecture

Hesabi follows a strict layered architecture, separating concerns cleanly across five layers:

```
Browser (HTML/CSS/JS)
        ↓  fetch() JSON
   API Layer (Flask Blueprints)
        ↓
  Service Layer (business logic + validation)
        ↓
 Repository Layer (data access only)
        ↓
   Database (SQLite)
```

| Layer | Responsibility |
|---|---|
| **Frontend** | Single-page app in vanilla JS. Fetches JSON from Flask, renders UI entirely in the browser. No server-side rendering. |
| **API Layer** | Receives HTTP requests, performs structural validation, returns JSON responses. Zero business logic. |
| **Service Layer** | Owns all business logic and domain validation. The sole authority for domain rules regardless of request origin. |
| **Repository Layer** | The only layer that talks to the database. Pure data access — no logic, no validation. Swappable without touching other layers. |
| **Database** | SQLite with foreign key constraints enforced at the schema level. |

---

## Tech Stack

| Area | Technology |
|---|---|
| Backend | Python 3.11, Flask, Flask-CORS |
| Database | SQLite (`sqlite3` — no ORM) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Containerization | Docker, Docker Compose |
| Reverse Proxy | Nginx |

---

## Project Structure

```
hesabi/
├── Dockerfile                  # Backend container recipe
├── docker-compose.yml          # Orchestrates backend + frontend containers
├── nginx.conf                  # Nginx reverse proxy config
├── requirements.txt
│
├── app/                        # Backend (Flask)
│   ├── app.py                  # Flask entry point — registers all blueprints
│   ├── main.py                 # App bootstrap — wires all layers together
│   ├── backend/
│   │   ├── conn_db.py          # SQLite connection
│   │   ├── setup_db.py         # Schema definition (3 tables)
│   │   ├── repository.py       # Data access layer
│   │   ├── service.py          # Business logic + validation layer
│   │   └── utils.py            # Shared helpers (text/date normalization)
│   └── api/
│       ├── transaction.py      # /api/transactions/ endpoints
│       ├── category.py         # /api/categories/ endpoints
│       ├── budget.py           # /api/budgets/ endpoints
│       └── compute.py          # /api/compute/ endpoints (balances)
│
└── frontend/                   # Frontend (served by Nginx)
    ├── index.html              # Single HTML file — all pages in one DOM
    ├── style.css               # Full responsive styling (desktop + mobile)
    └── app.js                  # All JS: state, routing, fetch, rendering
```

---

## How Docker and Nginx work together

```
Browser → localhost:8080
              ↓
           Nginx
          /      \
    /             /api/
(serves           (proxied to)
HTML/CSS/JS)    Flask :5000
                    ↓
                 SQLite
```

- **Backend container** — built from `Dockerfile`, runs Flask on port 5000
- **Frontend container** — uses official `nginx:alpine` image, no Dockerfile needed. Your frontend files and `nginx.conf` are mounted into it via Docker volumes.
- Nginx serves static files directly and forwards all `/api/` requests to the Flask container. The two containers communicate by Docker service name (`backend`) on an internal Docker network.

---

## Data Model

Three core entities:

- **Transaction** — a single income or expense record. Optionally linked to a category. Income transactions cannot reference a category (domain rule enforced at service layer).
- **Category** — a named spending bucket. Always created together with a budget (atomic operation — a category without a budget is meaningless in this domain).
- **Budget** — a monthly spending goal tied to exactly one category. Edited through the category form — no separate budget UI.

### Relationships

```
Category  1 ──── 1  Budget
Category  1 ──── *  Transaction
```

Foreign key behavior:
- Deleting a category → cascades to its budget (`ON DELETE CASCADE`)
- Deleting a category → sets `category_id` to NULL on its transactions (`ON DELETE SET NULL`)

---

## API Endpoints

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/transactions/` | List all transactions |
| POST | `/api/transactions/` | Add a transaction |
| PUT | `/api/transactions/<id>` | Edit a transaction |
| DELETE | `/api/transactions/<id>` | Delete a transaction |

### Categories
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/categories/` | List all categories (includes budget_goal) |
| POST | `/api/categories/` | Add a category + budget (atomic) |
| PUT | `/api/categories/<id>` | Edit category name and/or budget goal |
| DELETE | `/api/categories/<id>` | Delete category (cascades to budget) |

### Compute
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/compute/total` | Total balance (income − expenses) |
| GET | `/api/compute/income` | Total income |
| GET | `/api/compute/expense` | Total expenses |
| GET | `/api/compute/categories/balance` | Balance for all categories |
| GET | `/api/compute/category/<id>/balance` | Balance for one category |

---

## Running locally

**Requirements:** Docker and Docker Compose installed.

```bash
git clone https://github.com/muhammadkhajouei-web/hesabi.git
cd hesabi
docker-compose up --build
```

Open `http://localhost:8080` in your browser.

---

## Status

✅ Backend — complete and tested (all CRUD + compute endpoints)  
✅ Frontend — complete (all pages, add/edit/delete, mobile responsive)  
🔜 HTTPS setup via Certbot  
🔜 Deployment to production server  
🔜 Android "Add to Home Screen" (requires HTTPS)  

---

## Why this project

Hesabi is a practice project built while learning Python (~2 months in), aimed at applying real software architecture principles to a small but practically useful application: layered design, separation of concerns, RESTful API patterns, containerized deployment, and responsive frontend development — all from scratch without frameworks or shortcuts.

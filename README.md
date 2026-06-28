# Hesabi 💰

**Hesabi** (حسابی — "accounting" in Persian) is a personal finance tracking application that helps users record income and expenses, manage category-based budgets, and monitor real-time spending balances.

This project is being built as a hands-on learning exercise to practice clean backend architecture, RESTful API design, and full-stack development with Python and Flask.

---

## What it does

- Track income and expense transactions
- Organize spending into categories
- Set a budget goal for each category
- Calculate real-time balances:
  - Total income
  - Total expense
  - Overall remaining balance
  - Spending and remaining balance per category
  - Spending and remaining balance across all categories

---

## Architecture

Hesabi follows a layered architecture, separating concerns cleanly across four layers:

```
Frontend  →  API Layer  →  Service Layer  →  Repository Layer  →  Database (SQLite)
```

| Layer | Responsibility |
|---|---|
| **API Layer** | Receives HTTP requests, performs structural validation, returns JSON responses. No business logic. |
| **Service Layer** | Owns all business logic and domain validation. The only layer authorized to enforce domain rules. |
| **Repository Layer** | The only layer that talks to the database. Pure data access, no logic. |
| **Main** | Bootstraps the app once at startup — creates the DB connection, wires all layers together, and starts the server. |

This separation means the database engine, validation rules, and API framework can each evolve independently without breaking the others.

---

## Tech Stack

- **Backend:** Python, Flask (Blueprints)
- **Database:** SQLite
- **Frontend:** HTML/CSS/JavaScript *(in progress)*

---

## Project Structure

```
app/
├── layers/
│   ├── conn_db.py       # Database connection
│   ├── setup_db.py      # Schema definition
│   ├── repository.py    # Data access layer
│   ├── service.py       # Business logic layer
│   └── main.py          # App bootstrap
├── api/
│   ├── transaction.py   # Transaction endpoints
│   ├── category.py      # Category endpoints
│   ├── budget.py        # Budget endpoints
│   └── compute.py       # Calculation endpoints
└── frontend/
    ├── templates/
    └── static/
```

---

## Data Model

Three core entities:

- **Transaction** — a single income or expense record, optionally linked to a category
- **Category** — a spending category, always linked to a budget
- **Budget** — a spending goal tied to exactly one category

---

## Status

🚧 **Work in progress.** Backend (repository, service, and API layers) is functional and tested. Frontend is currently under development.

---

## Why this project

Hesabi is a practice project built while learning Python, aimed at applying real software architecture principles — layered design, separation of concerns, dependency injection, and RESTful API patterns — to a small but practically useful application.

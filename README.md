# 🧠 AI Finance Coach – Backend

Backend API for **AI Finance Coach**, a personal finance analytics and coaching MVP that helps users understand their spending habits, track income and expenses, and receive AI-powered financial insights.

This project is designed as a **real-world backend system**, not a demo app, with a clean architecture, analytics endpoints, and an AI integration layer.

---

## 🚀 Features

- Track **expenses** with categories and descriptions
- Track **income** from multiple sources
- Financial **analytics** with time-based filtering
- Detection of **spending patterns** and micro-expenses
- AI-powered **financial coaching insights**
- Clean REST API with interactive documentation

---

## 🧱 Tech Stack

- **Python 3.11**
- **FastAPI** – API framework
- **SQLAlchemy** – ORM
- **SQLite** – Local database (development)
- **OpenAI API** – AI-generated financial advice
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server

---

## 📂 Project Structure

backend/
│
├── app/
│ ├── main.py # FastAPI app entry point
│ │
│ ├── database.py # Database configuration & session
│ │
│ ├── models/ # SQLAlchemy models
│ │ ├── expense.py
│ │ └── income.py
│ │
│ ├── schemas/ # Pydantic schemas
│ │ ├── expense.py
│ │ └── income.py
│ │
│ ├── routes/ # API routes
│ │ ├── expenses.py
│ │ ├── income.py
│ │ └── analytics.py
│ │
│ └── services/ # Business logic & integrations
│ └── ai.py # OpenAI integration
│ └── insights.py # Financial insights generation
│
├── requirements.txt
├── .gitignore
└── README.md


---

## 📊 API Endpoints Overview

### Expenses
- `POST /expenses` – Create a new expense
- `GET /expenses` – List expenses (with filters)

### Income
- `POST /income` – Add income
- `GET /income` – List income records

### Analytics
- `GET /summary?days=30` – Financial summary for a time window
- `GET /analytics/summary?days=30` – Analytics + AI insights

All analytics endpoints support **time-based filtering** to avoid old data affecting current insights.

---

## 🤖 AI Financial Coaching

The AI layer analyzes:
- Spending distribution
- Income vs expenses ratio
- Micro-expense patterns
- Risk level based on recent behavior

It returns:
- A short financial summary
- Practical, realistic suggestions
- Action-oriented advice (not generic tips)

The AI logic is intentionally isolated in `services/ai.py`.

---

## ⚙️ Environment Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/ai-finance-coach-backend.git
cd ai-finance-coach-backend

### 2️⃣ Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

### 4️⃣ Set up environment variables
```bash
# Create a .env file in the root directory
# Add the following variables:
OPENAI_API_KEY=your_openai_api_key

### 5️⃣ Run the API
```bash
uvicorn app.main:app --reload

### 6️⃣ Access the API documentation
```bash
http://127.0.0.1:8000/docs
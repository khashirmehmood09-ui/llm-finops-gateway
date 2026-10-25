# 💸 LLM FinOps & Pre-Flight Guardrail Gateway

An enterprise-grade, decoupled AI microservice designed to estimate token consumption, latency, and exact API costs **before** sending prompts to expensive LLM endpoints (like GPT-4o or Claude). 

---

## 🚀 Problem Statement
In modern LLM application development, unexpected token spikes and latency bottlenecks can drastically inflate cloud infrastructure budgets. Developers often discover high costs *after* the API call is made. 

## 💡 The Solution
This project acts as a **Pre-Flight Guardrail Gateway**. It intercepts prompts, runs them through optimized Machine Learning regression models (Random Forest), and instantly forecasts:
- Input & Output Token Counts
- Expected Latency ($ms$)
- Estimated Cost (USD)

---

## 🏗️ Architecture & Tech Stack
This project follows a **Decoupled Headless Architecture**:
- **Backend:** FastAPI (Serving ML inference pipelines & cost calculation logic)
- **Frontend:** Streamlit (Clean, interactive client dashboard)
- **Machine Learning:** Scikit-Learn (Random Forest Regressors optimized with regularization to prevent overfitting)
- **Data Pipeline:** Custom dataset generation & feature engineering parsing prompt characteristics.

---

## 📊 Model Performance
- **Token Predictor Model:** Achieved an **$R^2$ Score of ~0.86**, indicating high accuracy in predicting output token lengths based on prompt structures.
- **Latency Forecaster:** Regularized Random Forest tuned to capture real-world network and inference variance.

---

## 🛠️ Project Structure
```text
regression/
│
├── app/
│   ├── main.py              # FastAPI backend entry point & prediction endpoints
│   └── frontend.py          # Streamlit user interface dashboard
├── models/                  # Trained joblib ML models & scalers
├── dataset/                 # Training and synthetic generation scripts
├── requirements.txt         # Project dependencies
└── README.md

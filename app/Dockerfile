# Official Python lightweight image
FROM python:3.10-slim

# Working directory set karo container ke andar
WORKDIR /app

# System dependencies agar koi zaroori hon
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Dependencies install karne ke liye requirements copy karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki poora project copy karo
COPY . .

# FastAPI port expose karo
EXPOSE 8000

# Server run karne ki command (Uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
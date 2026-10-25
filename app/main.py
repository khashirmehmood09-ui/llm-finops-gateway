import os
import json
import joblib
import tiktoken
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. Import CORSMiddleware
from pydantic import BaseModel, ConfigDict

# 1. Initialize FastAPI app
app = FastAPI(
    title="LLM FinOps & Latency Forecaster API",
    version="1.0.0",
    description="Production-grade microservice to predict LLM token consumption, latency, and costs."
)

# 🏭 2. Add CORS Middleware (Yeh zaroori hai Next.js connection ke liye!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development aur initial deployment ke liye sab origins allow hain
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS, etc. sab allow hain
    allow_headers=["*"],
)

# 2. Define Paths & Load Artifacts on Startup (Memory Caching)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
PRICING_FILE = os.path.join(BASE_DIR, "pricing_registry.json")

# Load Tokenizer
tokenizer = tiktoken.get_encoding("cl100k_base")

# Load Models globally (loaded once when server starts)
try:
    token_model_path = os.path.join(ARTIFACTS_DIR, "model_tokens.pkl")
    latency_model_path = os.path.join(ARTIFACTS_DIR, "model_latency.pkl")
    
    model_tokens = joblib.load(token_model_path)
    model_latency = joblib.load(latency_model_path)
    print("✅ ML Model artifacts loaded successfully into memory!")
except Exception as e:
    print(f"⚠️ Warning: Model artifacts not found. Please run train_model.py first! Error: {e}")

# Load Pricing Registry
def load_pricing():
    if os.path.exists(PRICING_FILE):
        with open(PRICING_FILE, "r") as f:
            return json.load(f)
    return {}

PRICING_REGISTRY = load_pricing()

# 3. Request Body Schema (Pydantic Validation with ConfigDict fix)
class PromptRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    prompt: str
    model_name: str  # e.g., "gpt-4o-mini", "claude-3-5-sonnet", "groq-llama3-8b"

# 4. API Endpoint: Predict Cost & Latency
@app.post("/predict-costs")
def predict_llm_metrics(payload: PromptRequest):
    # Check if model exists in pricing registry
    if payload.model_name not in PRICING_REGISTRY:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid model name. Available models: {list(PRICING_REGISTRY.keys())}"
        )
    
    # Step A: Extract exact input tokens locally using tiktoken
    input_tokens = len(tokenizer.encode(payload.prompt))
    
    # Step B: Predict output tokens using trained Scikit-Learn model
    predicted_output_tokens = float(model_tokens.predict([[input_tokens]])[0])
    predicted_output_tokens = max(5, int(predicted_output_tokens)) # Safety floor
    
    # Step C: Predict latency using input and output tokens
    predicted_latency = float(model_latency.predict([[input_tokens, predicted_output_tokens]])[0])
    predicted_latency = max(50.0, round(predicted_latency, 2))
    
    # Step D: Calculate cost dynamically using pricing registry
    model_rates = PRICING_REGISTRY[payload.model_name]
    input_cost = (input_tokens / 1000.0) * model_rates["input_per_1k"]
    output_cost = (predicted_output_tokens / 1000.0) * model_rates["output_per_1k"]
    total_cost_usd = round(input_cost + output_cost, 6)
    
    # Step E: Return structured JSON response
    return {
        "status": "success",
        "model_used": payload.model_name,
        "metrics": {
            "input_tokens": input_tokens,
            "predicted_output_tokens": predicted_output_tokens,
            "total_tokens": input_tokens + predicted_output_tokens,
            "estimated_latency_ms": predicted_latency,
            "estimated_cost_usd": total_cost_usd
        }
    }

@app.get("/")
def health_check():
    return {"status": "online", "service": "LLM FinOps & Latency Forecaster API"}
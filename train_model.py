import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def train_forecaster_models():
    data_path = os.path.join("data", "model_ready_data.csv")
    if not os.path.exists(data_path):
        print(f"❌ Error: Dataset not found at {data_path}. Please run generate_data.py first!")
        return

    print("📊 Loading dataset for production model training...")
    df = pd.read_csv(data_path)

    # Model 1: Predict Output Tokens using Random Forest
    print("\n--- Training Model 1: Token Predictor (Random Forest) ---")
    X_tok = df[['input_tokens']]
    y_tok = df['output_tokens']
    
    X_train_tok, X_test_tok, y_train_tok, y_test_tok = train_test_split(
        X_tok, y_tok, test_size=0.2, random_state=42
    )
    
    model_tokens = RandomForestRegressor(n_estimators=100, random_state=42)
    model_tokens.fit(X_train_tok, y_train_tok)
    print(f"✅ Token Model Train R² Score: {model_tokens.score(X_train_tok, y_train_tok):.4f}")
    print(f"✅ Token Model Test R² Score: {model_tokens.score(X_test_tok, y_test_tok):.4f}")

    # Model 2: Predict Latency using Input & Output Tokens (With Regularization)
    print("\n--- Training Model 2: Latency Forecaster (Random Forest with Regularization) ---")
    X_lat = df[['input_tokens', 'output_tokens']]
    y_lat = df['latency_ms']
    
    X_train_lat, X_test_lat, y_train_lat, y_test_lat = train_test_split(
        X_lat, y_lat, test_size=0.2, random_state=42
    )
    
    # Regularization parameters to control overfitting on noisy latency data
    model_latency = RandomForestRegressor(
        n_estimators=100, 
        max_depth=6,             # Trees ko bohot gehra (deep) hone se rokta hai
        min_samples_split=10,    # Leaf nodes par minimum samples ki limit lagata hai
        random_state=42
    )
    model_latency.fit(X_train_lat, y_train_lat)
    print(f"✅ Latency Model Train R² Score: {model_latency.score(X_train_lat, y_train_lat):.4f}")
    print(f"✅ Latency Model Test R² Score: {model_latency.score(X_test_lat, y_test_lat):.4f}")

    # Save Model Binaries to app/artifacts/
    artifacts_dir = os.path.join("app", "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    joblib.dump(model_tokens, os.path.join(artifacts_dir, "model_tokens.pkl"))
    joblib.dump(model_latency, os.path.join(artifacts_dir, "model_latency.pkl"))

    print(f"\n🎯 Success! Upgraded model artifacts saved and serialized in {artifacts_dir}/")

if __name__ == "__main__":
    train_forecaster_models()
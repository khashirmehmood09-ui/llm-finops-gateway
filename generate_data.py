import os
import pandas as pd
import tiktoken
import numpy as np

# Initialize Tokenizer (OpenAI cl100k_base encoding)
tokenizer = tiktoken.get_encoding("cl100k_base")

def generate_production_dataset():
    # Real-world enterprise and developer prompt categories
    categories = {
        "code_generation": [
            "Write a Python FastAPI application with JWT authentication, rate limiting, and PostgreSQL integration using SQLAlchemy.",
            "Debug this React useEffect hook infinite loop issue and optimize the component re-render performance.",
            "Write a complex PySpark data pipeline script to process 10 million rows of streaming JSON data, handle missing values, and write to delta lake.",
            "Create a Dockerfile and docker-compose.yml configuration for a multi-container microservice architecture running Flask, Redis, and Celery workers."
        ],
        "data_science": [
            "Explain how transformer attention mechanism works in Large Language Models step by step with mathematical intuition.",
            "Write a complete Scikit-Learn machine learning pipeline featuring StandardScaler, OneHotEncoder, cross-validation, and hyperparameter tuning using Optuna.",
            "How do you handle severe class imbalance in a fraud detection dataset using SMOTE and custom evaluation metrics like PR-AUC?"
        ],
        "business_finops": [
            "Analyze the cost implications of scaling an LLM gateway from 10,000 daily active users to 1 million, comparing OpenAI GPT-4o with self-hosted Llama-3 on AWS EC2.",
            "Write an executive summary report on the ROI of implementing automated customer support AI agents for an e-commerce enterprise."
        ],
        "general_chat": [
            "Hi",
            "What is AI?",
            "Explain quantum computing in simple terms for a 10-year-old child.",
            "Translate the following technical English paragraph into fluent French and summarize it in three bullet points."
        ]
    }

    data = []
    np.random.seed(42) # Reproducible randomness for realistic variance

    # Generate a massive, diverse dataset simulating real production traffic
    print("🔄 Generating production-grade dataset from multi-domain prompt distributions...")
    
    for category, prompts in categories.items():
        for base_prompt in prompts:
            # Create variations to simulate real user typing and prompt engineering variety
            for i in range(150): # 150 variations per prompt to build a robust 1500+ rows dataset
                
                # Add dynamic suffix or prefix variations
                if i % 3 == 0:
                    modified_prompt = base_prompt + f" Make sure to include best practices and production considerations for version {i}. Context id: {np.random.randint(1000, 9999)}"
                elif i % 3 == 1:
                    modified_prompt = f"Please act as a senior architect. " + base_prompt
                else:
                    modified_prompt = base_prompt

                input_tokens = len(tokenizer.encode(modified_prompt))
                
                # Realistic token growth factor based on category complexity
                if category == "code_generation":
                    output_tokens = int(input_tokens * np.random.uniform(2.5, 4.0) + np.random.normal(0, 15))
                elif category == "data_science":
                    output_tokens = int(input_tokens * np.random.uniform(2.0, 3.2) + np.random.normal(0, 10))
                else:
                    output_tokens = int(input_tokens * np.random.uniform(1.2, 2.0) + np.random.normal(0, 5))
                
                output_tokens = max(10, output_tokens)
                
                # Realistic latency simulation (Network overhead + Token generation time)
                # Latency scales primarily with total tokens generated plus system jitter
                latency_ms = round(120.0 + (input_tokens * 0.08) + (output_tokens * 0.45) + np.random.normal(0, 25), 2)
                latency_ms = max(80.0, latency_ms)

                data.append({
                    "prompt": modified_prompt,
                    "category": category,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "latency_ms": latency_ms
                })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df_dataset = generate_production_dataset()
    
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "model_ready_data.csv")
    df_dataset.to_csv(output_path, index=False)
    
    print(f"✅ Success! Generated professional dataset with {len(df_dataset)} rows and saved to {output_path}")
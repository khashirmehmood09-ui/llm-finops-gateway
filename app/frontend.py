import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="LLM FinOps & Cost Estimator",
    page_icon="💸",
    layout="centered"
)

# App Header
st.title("💸 LLM FinOps & Pre-Flight Guardrail Gateway")
st.markdown("""
Welcome to your enterprise LLM cost optimization dashboard. 
Estimate token consumption, expected latency, and exact API costs **before** hitting expensive LLM endpoints.
""")

st.divider()

# Sidebar for Model Selection & Settings
st.sidebar.header("⚙️ Configuration")
selected_model = st.sidebar.selectbox(
    "Select LLM Model",
    ["gpt-4o-mini", "gpt-4o", "claude-3-5-sonnet", "groq-llama3-8b"]
)

st.sidebar.info("""
**Pro-Tip:** Use this gateway as a pre-flight check in your production pipeline to prevent unexpected API budget spikes!
""")

# Main Input Area
prompt_text = st.text_area(
    "✍️ Enter your prompt or system instructions here:",
    placeholder="e.g., Write a complex Python script using asyncio and websockets...",
    height=150
)

# Predict Button
if st.button("🚀 Analyze & Estimate Cost", type="primary"):
    if not prompt_text.strip():
        st.warning("⚠️ Please enter a valid prompt first!")
    else:
        # FastAPI Backend Endpoint
        API_URL = "http://127.0.0.1:8000/predict-costs"
        
        payload = {
            "prompt": prompt_text,
            "model_name": selected_model
        }
        
        try:
            with st.spinner("Analyzing tokens and forecasting latency..."):
                response = requests.post(API_URL, json=payload, timeout=10)
                
            if response.status_code == 200:
                res_data = response.json()
                metrics = res_data["metrics"]
                
                st.success("✅ Analysis Complete!")
                
                # Metrics Display Layout
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(label="Input Tokens", value=metrics["input_tokens"])
                with col2:
                    st.metric(label="Predicted Output Tokens", value=metrics["predicted_output_tokens"])
                with col3:
                    st.metric(label="Total Tokens", value=metrics["total_tokens"])
                
                st.divider()
                
                # Cost & Latency Highlight
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.metric(
                        label="Estimated Latency", 
                        value=f"{metrics['estimated_latency_ms']} ms"
                    )
                with col_res2:
                    st.metric(
                        label="Estimated Total Cost", 
                        value=f"${metrics['estimated_cost_usd']:.6f}"
                    )
                    
            else:
                st.error(f"❌ API Error: {response.json().get('detail', 'Unknown error')}")
                
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            st.error("🚨 Connection Error: Could not connect to FastAPI backend. Is your server running on port 8000?")
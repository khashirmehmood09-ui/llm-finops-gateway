import streamlit as st
import requests

# 1. Page Configuration (Wide layout for professional dashboard feel)
st.set_page_config(
    page_title="LLM FinOps & Latency Forecaster",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Styling for Dark Theme SaaS Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput textarea, .stSelectbox select {
        background-color: #161b22;
        color: #c9d1d9;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Initialize Session State for History Tracking (Session Ledger)
if "history" not in st.session_state:
    st.session_state.history = []

# 4. Sidebar Configuration (Clean & Professional UI without broken external images)
with st.sidebar:
    st.markdown("### ⚡ AI FinOps Gateway")
    st.markdown("---")
    st.title("⚙️ Config Panel")
    
    # Model Selection matching backend PRICING_REGISTRY
    selected_model = st.selectbox(
        "Select Target LLM Model",
        ["gpt-4o-mini", "claude-3-5-sonnet", "groq-llama3-8b"],
        help="Choose the model to estimate token consumption, latency, and cost."
    )
    
    st.markdown("---")
    st.markdown("### 📊 FinOps Guardrails")
    st.info("Pre-flight cost estimation helps enterprise applications prevent budget overruns and unexpected API latencies.")

# 5. Main Dashboard Header
st.title("⚡ LLM FinOps & Latency Forecaster")
st.markdown("Enterprise Pre-Flight Cost Estimation, Token Accounting & Latency Prediction Gateway.")
st.markdown("---")

# 6. User Input Section
prompt_text = st.text_area(
    "Enter Proposed LLM Prompt / Query:",
    placeholder="e.g., Write a comprehensive Python script to parse large JSON datasets and optimize memory usage...",
    height=150
)

# Backend FastAPI Endpoint URL (Local connection)
API_URL = "https://llm-finops-gateway.onrender.com/predict-costs"

col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    analyze_btn = st.button("🚀 Analyze Prompt", use_container_width=True)

if analyze_btn:
    if not prompt_text.strip():
        st.warning("⚠️ Please enter a valid prompt before analyzing.")
    else:
        with st.spinner("🔄 Inspecting prompt tokens, forecasting latency, and calculating cost..."):
            try:
                payload = {
                    "prompt": prompt_text,
                    "model_name": selected_model
                }
                
                # Sending POST request to FastAPI backend
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    metrics = data["metrics"]
                    
                    st.success("✅ Analysis Complete! Pre-flight metrics calculated successfully.")
                    st.markdown("### 📈 Estimated Consumption & Performance")
                    
                    # 7. Display Metrics in Professional Columns
                    m1, m2, m3, m4, m5 = st.columns(5)
                    
                    with m1:
                        st.metric(label="Input Tokens", value=f"{metrics['input_tokens']:,}")
                    with m2:
                        st.metric(label="Predicted Output", value=f"{metrics['predicted_output_tokens']:,}")
                    with m3:
                        st.metric(label="Total Tokens", value=f"{metrics['total_tokens']:,}")
                    with m4:
                        st.metric(label="Est. Latency", value=f"{metrics['estimated_latency_ms']} ms")
                    with m5:
                        st.metric(label="Est. Cost (USD)", value=f"${metrics['estimated_cost_usd']:.6f}")
                        
                    # 8. Append to Session State History Ledger
                    st.session_state.history.insert(0, {
                        "Model": selected_model,
                        "Prompt Snippet": prompt_text[:40] + "...",
                        "Input": metrics['input_tokens'],
                        "Output": metrics['predicted_output_tokens'],
                        "Total": metrics['total_tokens'],
                        "Latency (ms)": metrics['estimated_latency_ms'],
                        "Cost (USD)": f"${metrics['estimated_cost_usd']:.6f}"
                    })
                    
                    # Detailed JSON view expander for technical transparency
                    with st.expander("🔍 View Raw API Response JSON"):
                        st.json(data)
                        
                else:
                    error_detail = response.json().get("detail", "Unknown error occurred.")
                    st.error(f"❌ API Error ({response.status_code}): {error_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🔌 Failed to connect to FastAPI backend. Make sure your backend server is running (`uvicorn app.main:app --reload`).")
            except Exception as e:
                st.error(f"⚠️ An unexpected error occurred: {e}")

# 9. Display Session History Ledger Table
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 🕒 Recent Prompt History (Session Ledger)")
    st.markdown("Yeh table aapke current session ke saare prompt analyses ka record maintain karta hai.")
    st.dataframe(st.session_state.history, use_container_width=True)
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
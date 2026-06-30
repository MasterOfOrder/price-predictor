import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from src.bot_logic import get_bot_response
except ImportError:
    from bot_logic import get_bot_response

st.set_page_config(
    page_title="AI Predictive Hardware Assistant",
    page_icon="🔮",
    layout="centered"
)

st.title("🔮 Predictive Tech Hardware Assistant")
st.write("Enter a product URL and ask our AI to analyze real-time market trends and generate predictive buying verdicts.")

st.markdown("---")

product_url = st.text_input(
    "🔗 Product Link", 
    placeholder="Paste your product URL here (e.g., https://www.pcpartpicker.com/product/rtx5080)..."
)

user_message = st.text_input(
    "💬 What would you like to ask?", 
    placeholder="e.g., Can you predict the price trend for this next week?"
)

if st.button("Analyze & Forecast", type="primary"):
    if not user_message.strip():
        st.warning("Please enter a question or greeting for the AI assistant.")
    else:
        with st.spinner("AI is evaluating intent and running predictive regressions..."):
            bot_reply = get_bot_response(user_message, product_url=product_url if product_url.strip() else None)
            
        st.markdown("### 🤖 Assistant Response")
        
        if "Sorry, I couldn't fetch data from this URL" in bot_reply or "Please provide the product URL" in bot_reply:
            st.error(bot_reply)
        elif "📊 **Product ID:**" in bot_reply:
            # Displays the success payload in a beautiful callout box
            st.success("Analysis Complete!")
            st.markdown(bot_reply)
        else:
            # Handles general greetings or standard conversational text
            st.info(bot_reply)

st.markdown("---")
st.caption("⚡ Powered by Zero-Shot NLP Classification & In-Memory Linear Regression Time-Series Forecasting.")

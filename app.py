import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = st.secrets.get("MISTRAL_API_KEY", "QcwdNlmfqQulxAbH9HAucYtt1AW5VePj")

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # සිංහල නිවැරදිව ලබා ගැනීමට වැඩිදියුණු කළ උපදෙස් (Prompt Engineering)
    system_instruction = (
        "You are an expert Sinhala translator and fact-checker. "
        "The user will provide input in Singlish or Sinhala. "
        "Strictly follow these rules:\n"
        "1. Identify the core question and translate it to English first for internal reasoning.\n"
        "2. Find the most accurate factual answer.\n"
        "3. Provide the final response ONLY in natural, grammatically correct Sinhala Unicode.\n"
        "4. Avoid direct word-to-word translations from English; use phrases a Sri Lankan would naturally use.\n"
        "5. Keep the answer concise (max 2 sentences)."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Answer this accurately in Sinhala: {user_input}"}
        ],
        "temperature": 0.1 # නිවැරදි දත්ත ලබා ගැනීමට මෙය අඩු මට්ටමක තැබීම සුදුසුයි
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception:
        return "දත්ත ලබා ගැනීමේදී දෝෂයක් සිදු විය. කරුණාකර නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🇱🇰")

st.markdown("<h2 style='text-align: center;'>නිවැරදි සිංහල AI සහායකයා</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ප්‍රශ්නය මෙතන ලියන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("පිළිතුර සකසමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

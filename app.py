import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# https://console.groq.com/ එකෙන් ගත්ත API Key එක මෙතනට දාන්න
GROQ_API_KEY = "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"

def get_groq_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-70b-versatile", # සිංහල සඳහා ඉතා දක්ෂ model එකක්
        "messages": [
            {"role": "system", "content": "You are a professional Sinhala AI assistant. Answer in natural Sinhala Unicode."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "දෝෂයක් සිදු විය. කරුණාකර නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala Free AI", page_icon="🇱🇰")
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>නොමිලේ සිංහල AI (Groq)</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("සිංහලෙන් අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = get_groq_response(prompt)
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

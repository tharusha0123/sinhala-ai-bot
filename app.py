import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# https://console.groq.com/ එකෙන් ගත්ත API Key එක මෙතනට දාන්න
# නැත්නම් Streamlit Secrets වල 'GROQ_API_KEY' ලෙස ඇතුළත් කරන්න.
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "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")

def get_groq_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.1-70b-versatile", # සිංහල සඳහා හොඳම Model එක
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional Sinhala AI assistant. Provide accurate answers in natural Sinhala Unicode. If asked in Singlish, still answer in proper Sinhala."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"දෝෂයක් සිදු විය: {str(e)}"

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI (Groq)", page_icon="🇱🇰")

# Interface එක ලස්සන කිරීමට CSS
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

# Chat History පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_groq_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

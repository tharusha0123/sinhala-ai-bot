import streamlit as st
import requests
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION ---
GROQ_API_KEY = "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"

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_at6miz9j.json")

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # මෙතන තමයි නම සහ හඳුන්වා දීම වෙනස් කරන්නේ
    system_instruction = (
        "Your name is 'සිංහල Chat Bot'. You are a professional Sinhala AI assistant created by Tharusha Rathnayake. "
        "Instructions:\n"
        "1. Always introduce yourself as 'සිංහල Chat Bot' if asked for your name.\n"
        "2. Respond only in natural and accurate Sinhala Unicode.\n"
        "3. Understand English, Singlish, and Sinhala perfectly but always reply in Sinhala.\n"
        "4. Be helpful, friendly, and polite."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.4 
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, දත්ත ලබා ගැනීමේදී ගැටලුවක් මතු විය."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="සිංහල Chat Bot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp { background-color: #0e1117; animation: fadeIn 1.5s ease-out; }
    .main-title {
        font-size: 60px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #00ff88, #0055ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        margin-top: -30px;
    }
    @keyframes shine { to { background-position: 200% center; } }
    .footer { text-align: center; font-size: 16px; color: #00ff88; font-weight: bold; }
    .stChatMessage { border-radius: 20px !important; transition: transform 0.3s ease; }
    .stChatMessage:hover { transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_ai:
        st_lottie(lottie_ai, height=200, key="ai_anim")

st.markdown("<h1 class='main-title'>සිංහල Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("සිංහලෙන් හෝ English වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

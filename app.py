import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
import re

GROQ_API_KEY = "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"

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

lottie_ai = load_lottieurl("https://lottie.host/880280a3-f09b-449e-953e-51c36093867c/m76Y9Y9H6C.json")

def get_ai_response(messages_history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    system_msg = {
        "role": "system", 
        "content": (
            "Your name is 'සිංහල Chat Bot', created by Tharusha Rathnayake. "
            "GREETING RULE: If the user says 'hi', 'hello', or any common greeting, ONLY respond with: 'මම සිංහල Chat Bot, මම කොහොමද ඔබට උදව් කරන්නේ?' "
            "MULTIMEDIA RULE: NEVER provide YouTube links or video players. Do not show videos. "
            "IMAGE RULE: Provide clear Markdown links for images or info websites if relevant. "
            "Tone: Be friendly and conversational like Gemini. Ensure natural Sinhala grammar. "
            "Engagement: Always end with a helpful question to keep the chat going."
        )
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [system_msg] + messages_history,
        "temperature": 0.6 
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයක්: {str(e)}"

st.set_page_config(page_title="සිංහල Chat Bot Pro", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    @keyframes superFadeIn {
        0% { opacity: 0; transform: translateY(30px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    [data-testid="stAppViewContainer"] { 
        background: radial-gradient(circle at top right, #1a202c, #0e1117) !important; 
        color: white !important;
        animation: superFadeIn 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stAppViewContainer"] { background: #ffffff !important; color: #1a202c !important; }
        .stMarkdown, p, h1, h2, h3, span { color: #1a202c !important; }
    }

    .main-title { 
        font-size: clamp(35px, 6vw, 65px) !important; 
        font-weight: 900; 
        text-align: center; 
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab); 
        background-size: 400% 400%; 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        animation: gradientBG 8s ease infinite; 
    }

    @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }
    .footer { text-align: center; font-size: 14px; color: #00ff88; font-weight: bold; margin-bottom: 20px; letter-spacing: 1.5px; }
    
    div[data-testid="stChatMessage"] { 
        border-radius: 25px !important; 
        border: 1px solid rgba(255, 255, 255, 0.15); 
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px); 
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        animation: superFadeIn 0.8s ease-out;
    }
    div[data-testid="stChatMessage"]:hover { transform: translateY(-8px) scale(1.02); border-color: #00d4ff; }
    
    .stButton button { padding: 2px 8px !important; font-size: 12px !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": "හායි! මම සිංහල Chat Bot. අද මම ඔබට උදව් කරන්නේ කොහොමද?"}]
        st.session_state.feedback = {}
        st.rerun()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_ai: st_lottie(lottie_ai, height=180, key="ai_anim")

st.markdown("<h1 class='main-title'>සිංහල Chat Bot Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "හායි! මම සිංහල Chat Bot. ඔයාට ඕනෑම ප්‍රශ්නයක් සිංහලෙන් හෝ English වලින් අහන්න, මම සිංහලෙන් උත්තර දෙන්නම්. අද අපි මොනවා ගැනද කතා කරන්නේ?"}]
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and i > 0:
            if i in st.session_state.feedback:
                st.write("✅")
            else:
                c1, c2, c3 = st.columns([0.04, 0.04, 0.92])
                with c1: 
                    if st.button("👍", key=f"up_{i}"):
                        st.session_state.feedback[i] = True
                        st.rerun()
                with c2: 
                    if st.button("👎", key=f"down_{i}"):
                        st.session_state.feedback[i] = True
                        st.rerun()

if prompt := st.chat_input("සිංහලෙන් හෝ English වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        with st.spinner("සිතමින් පවතී..."):
            full_response = get_ai_response(st.session_state.messages)
            typed_text = ""
            for char in full_response:
                typed_text += char
                placeholder.markdown(typed_text + "▌")
                time.sleep(0.005)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()

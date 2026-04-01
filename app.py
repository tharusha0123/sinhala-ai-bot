import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ Groq API Key එක ඇතුළත් කරන්න
GROQ_API_KEY = "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"

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# Robot Animation එක
lottie_ai = load_lottieurl("https://lottie.host/880280a3-f09b-449e-953e-51c36093867c/m76Y9Y9H6C.json")

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    system_instruction = (
        "Your name is 'සිංහල Chat Bot', created by Tharusha Rathnayake. "
        "Rules: Always respond in natural Sinhala Unicode. Be friendly. Understand Singlish."
    )
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": user_input}],
        "temperature": 0.4 
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except: return "සම්බන්ධතාවයේ දෝෂයක්. නැවත උත්සාහ කරන්න."

# --- 2. ADVANCED UI DESIGN (Light/Dark Responsive) ---
st.set_page_config(page_title="සිංහල Chat Bot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* Dark & Light Mode 100% Fix */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #1a202c, #0e1117) !important;
        color: white !important;
        transition: all 0.5s ease;
    }
    
    @media (prefers-color-scheme: light) {
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top right, #f7fafc, #ffffff) !important;
            color: #1a202c !important;
        }
        .stMarkdown, p, span, label, h1, h2, h3 {
            color: #1a202c !important;
        }
        .stChatInput textarea {
            color: #1a202c !important;
            background-color: #f0f2f6 !important;
        }
    }

    /* Gradient Title Animation */
    .main-title {
        font-size: clamp(40px, 8vw, 65px) !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientBG 8s ease infinite;
        margin-bottom: 5px;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .footer {
        text-align: center;
        font-size: 16px;
        color: #00ff88;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0,255,136,0.3);
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    /* Chat Messages Glassmorphism Animation */
    div[data-testid="stChatMessage"] {
        border-radius: 25px !important;
        border: 1px solid rgba(128, 128, 128, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    div[data-testid="stChatMessage"]:hover {
        transform: scale(1.02) translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_ai: st_lottie(lottie_ai, height=200, key="ai_anim")

st.markdown("<h1 class='main-title'>සිංහල Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    # ඔයා ඉල්ලපු විදිහට Welcome Message එක වෙනස් කළා
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "හායි! මම සිංහල Chat Bot. ඔයාට ඕනෑම ප්‍රශ්නයක් සිංහලෙන් හෝ English වලින් අහන්න, මම සිංහලෙන් උත්තර දෙන්නම්."
        }
    ]

# මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("සිංහලෙන් හෝ English වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty() # Typing effect එකක් පෙන්වීමට
        with st.spinner("සිතමින් පවතී..."):
            full_response = get_ai_response(prompt)
            
            # Typing animation effect
            typed_text = ""
            for char in full_response:
                typed_text += char
                placeholder.markdown(typed_text + "▌")
                time.sleep(0.005) # වේගය වෙනස් කරන්න පුළුවන්
            placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})

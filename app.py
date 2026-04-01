import streamlit as st
import requests
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION ---
GROQ_API_KEY = "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"

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except:
        return None

# ලස්සන අලුත් Robot Animation එකක්
lottie_ai = load_lottieurl("https://lottie.host/880280a3-f09b-449e-953e-51c36093867c/m76Y9Y9H6C.json")

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    
    system_instruction = (
        "Your name is 'සිංහල Chat Bot', created by Tharusha Rathnayake. "
        "Rules: 1. If user says 'hi' or 'hello', always reply: 'හායි! මම සිංහල Chat Bot. මම කොහොමද අද ඔබට උදව් කරන්නේ?' "
        "2. Always respond in high-quality Sinhala Unicode. 3. Be friendly and professional."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": system_instruction}, {"role": "user", "content": user_input}],
        "temperature": 0.4 
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, සම්බන්ධතාවයේ දෝෂයක්. නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN (Light/Dark Responsive) ---
st.set_page_config(page_title="සිංහල Chat Bot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* Light & Dark Mode එකට වර්ණ වෙනස් වීම */
    :root {
        --text-color: #ffffff;
        --bg-color: #0e1117;
        --accent-color: #00d4ff;
    }

    @media (prefers-color-scheme: light) {
        :root {
            --text-color: #1a202c;
            --bg-color: #f7fafc;
            --accent-color: #0055ff;
        }
    }

    /* පිටුව පෑදීගෙන එන Animation එක */
    .stApp {
        background-color: var(--bg-color);
        transition: all 0.5s ease;
    }

    /* ප්‍රධාන මාතෘකාව - Moving Gradient */
    .main-title {
        font-size: clamp(40px, 8vw, 65px) !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientBG 10s ease infinite;
        margin-top: -30px;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .footer {
        text-align: center;
        font-size: clamp(12px, 2vw, 16px);
        color: var(--accent-color);
        font-weight: bold;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Chat Bubbles - Glassmorphism style */
    .stChatMessage {
        border-radius: 20px !important;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# Animation එක පෙන්වීම
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if lottie_ai:
        st_lottie(lottie_ai, height=220, key="ai_anim", speed=1)

st.markdown("<h1 class='main-title'>සිංහල Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "හායි! මම සිංහල Chat Bot. ඔබට ඕනෑම ප්‍රශ්නයක් සිංහලෙන් හෝ English වලින් මගෙන් අසන්න. මම සිංහලෙන් ඔබට ඒ දේවල් පැහැදිලි කර දෙන්නම්."}
    ]

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

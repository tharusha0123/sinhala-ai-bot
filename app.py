import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
import uuid

# --- CONFIGURATION ---
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
            "HIGHLIGHT RULE: Always state the main factual answer clearly at the beginning in **BOLD**. "
            "1. Be friendly, conversational, and helpful. Use natural Sinhala Unicode. "
            "2. MEMORY: Remember previous details mentioned by the user. "
            "3. RESPONSE: Short for simple facts, detailed for broad topics. "
            "4. GREETING: If user says 'hi' or 'hello', ONLY respond with: 'මම සිංහල Chat Bot, මම කොහොමද ඔබට උදව් කරන්නේ?' "
            "5. NO YOUTUBE: Never provide YouTube links. "
            "6. ENGAGEMENT: Always end with a friendly question."
        )
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [system_msg] + messages_history,
        "temperature": 0.7 
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        return response.json()['choices'][0]['message']['content']
    except: return "සම්බන්ධතාවයේ දෝෂයක්. කරුණාකර නැවත උත්සාහ කරන්න."

# --- UI DESIGN & ANIMATIONS ---
st.set_page_config(page_title="සිංහල Chat Bot Pro", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    /* Fade-in Animation */
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stAppViewContainer"] { 
        background: radial-gradient(circle at top right, #1a202c, #0e1117) !important; 
        color: white !important;
        animation: fadeInSlide 1s ease-out;
    }

    .main-title { 
        font-size: clamp(28px, 7vw, 55px) !important; 
        font-weight: 900; 
        text-align: center; 
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab); 
        background-size: 400% 400%; 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        animation: gradientBG 8s ease infinite; 
    }

    @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    div[data-testid="stChatMessage"] { 
        border-radius: 18px !important; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        background: rgba(255, 255, 255, 0.04) !important;
        backdrop-filter: blur(10px); 
        transition: 0.3s;
        animation: fadeInSlide 0.6s ease-out;
    }
    
    div[data-testid="stChatMessage"]:hover { 
        transform: translateY(-3px); 
        border-color: rgba(0, 212, 255, 0.4); 
    }

    /* Like/Unlike Buttons Styling */
    .stButton button {
        padding: 0px !important;
        font-size: 14px !important;
        height: 26px !important;
        width: 32px !important;
        min-height: 26px !important;
        border-radius: 6px !important;
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100% !important;
        border-radius: 10px !important;
    }

    .new-chat-btn button {
        background-color: #2ecc71 !important;
        color: white !important;
        font-weight: bold !important;
        height: 45px !important;
    }

    strong { color: #00ff88 !important; }
    [data-testid="stSidebar"] { background-color: #11151c !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION INITIALIZATION ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.all_chats[new_id] = {
        "name": "Chat 1",
        "messages": [{"role": "assistant", "content": "හායි! මම සිංහල Chat Bot. අද මම ඔබට උදව් කරන්නේ කොහොමද?"}],
        "feedback": {}
    }

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=70)
    st.title("Chat Bot Pro")
    st.write("---")
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        chat_count = len(st.session_state.all_chats) + 1
        st.session_state.all_chats[new_id] = {
            "name": f"Chat {chat_count}",
            "messages": [{"role": "assistant", "content": "හායි! මම සිංහල Chat Bot. අද මම ඔබට උදව් කරන්නේ කොහොමද?"}],
            "feedback": {}
        }
        st.session_state.current_chat_id = new_id
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("---")
    st.subheader("📜 History")
    for chat_id, chat_data in st.session_state.all_chats.items():
        if st.button(f"💬 {chat_data['name']}", key=chat_id):
            st.session_state.current_chat_id = chat_id
            st.rerun()
    st.write("---")
    if st.button("🗑️ Clear All History"):
        st.session_state.all_chats = {}
        del st.session_state.current_chat_id
        st.rerun()

# --- MAIN DISPLAY ---
current_chat = st.session_state.all_chats[st.session_state.current_chat_id]
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    if lottie_ai: st_lottie(lottie_ai, height=130, key="ai_anim")
    st.markdown("<h1 class='main-title'>සිංහල Chat Bot Pro</h1>", unsafe_allow_html=True)

for i, message in enumerate(current_chat["messages"]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and i > 0:
            if i in current_chat["feedback"]:
                st.write("✅")
            else:
                btn_col1, btn_col2, _ = st.columns([0.05, 0.05, 0.9])
                with btn_col1:
                    if st.button("👍", key=f"up_{i}_{st.session_state.current_chat_id}"):
                        current_chat["feedback"][i] = True
                        st.rerun()
                with btn_col2:
                    if st.button("👎", key=f"down_{i}_{st.session_state.current_chat_id}"):
                        current_chat["feedback"][i] = True
                        st.rerun()

if prompt := st.chat_input("සිංහලෙන් හෝ English වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    current_chat["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        with st.spinner("සිතමින් පවතී..."):
            full_response = get_ai_response(current_chat["messages"])
            typed_text = ""
            for char in full_response:
                typed_text += char
                placeholder.markdown(typed_text + "▌")
                time.sleep(0.005)
            placeholder.markdown(full_response)
            current_chat["messages"].append({"role": "assistant", "content": full_response})
            st.rerun()

import streamlit as st
import requests

# --- 1. CONFIGURATION ---
GROQ_API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Singlish රටාවන් හඳුනාගැනීමට දෙන උදාහරණ සහිත උපදෙස්
    system_instruction = (
        "You are an advanced Sinhala AI. You have a deep understanding of 'Singlish' (Sinhala written in Roman/English characters).\n"
        "Rules:\n"
        "1. ALWAYS respond in natural Sinhala Unicode, regardless of the input language.\n"
        "2. Recognize Singlish patterns like: 'mkkd' -> 'මොකක්ද', 'khmda' -> 'කොහොමද', 'oyata' -> 'ඔයාට', 'nk' -> 'නැහැ', 'wada' -> 'වැඩ'.\n"
        "3. Understand variations like 'u' instead of 'o' (e.g., 'mukkda' or 'mukadda').\n"
        "4. If the user asks 'Oya mkkd karanne?', understand it as 'ඔයා මොකක්ද කරන්නේ?' and reply in Sinhala.\n"
        "5. If the input is pure English, still reply in Sinhala.\n"
        "6. Maintain high-quality grammar and friendly tone."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5 # Singlish අනුමාන කිරීමට 0.5 හෝ 0.6 ඉතා හොඳයි
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, දත්ත ලබා ගැනීමේදී ගැටලුවක් මතු විය. කරුණාකර නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="සිංහල Chat Bot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .main-title {
        font-size: 55px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00d4ff, #0055ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -50px;
        margin-bottom: 5px;
    }
    .footer {
        text-align: center;
        font-size: 16px;
        color: #8892b0;
        font-style: italic;
        margin-bottom: 30px;
    }
    .stChatMessage {
        border-radius: 20px !important;
        background-color: #1a202c !important;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("සිංහලෙන්, Singlish වලින් හෝ English වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

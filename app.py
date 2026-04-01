import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ Groq API Key එක ඇතුළත් කරන්න
GROQ_API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # භාෂා තුනම (Sinhala, Singlish, English) හොඳින් තේරුම් ගැනීමට දෙන උපදෙස්
    system_instruction = (
        "You are a professional and versatile AI assistant. "
        "The user will communicate in Sinhala Unicode, Singlish, or English. "
        "Your rules:\n"
        "1. If the user asks in Sinhala or Singlish, always respond in natural and grammatically correct Sinhala Unicode.\n"
        "2. If the user asks in English, you should still respond in Sinhala, but keep the explanation clear and accurate.\n"
        "3. Understand colloquial terms and various Singlish spellings (e.g., 'mkkd', 'mokakda', 'what').\n"
        "4. Be helpful, friendly, and provide high-quality information."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5 
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
        border: 1px solid #1e293b;
        border-radius: 20px !important;
        background-color: #1a202c !important;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# මාතෘකාව සහ Creator නම
st.markdown("<h1 class='main-title'>සිංහල Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ඔයා ඉල්ලපු වෙනස මෙතන තියෙනවා:
if prompt := st.chat_input("සිංහලෙන්, Singlish වලින් හෝ English වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

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
    
    # Singlish අඳුනා ගැනීමට දෙන විශේෂ උපදෙස් මාලාව
    system_instruction = (
        "You are an expert Sinhala AI assistant who perfectly understands Singlish (Sinhala written in English letters). "
        "Instructions:\n"
        "1. When a user sends a message in Singlish (e.g., 'mkkd wenne', 'kohomada', 'oya kawda'), "
        "first translate it internally to Sinhala context and then answer in high-quality Sinhala Unicode.\n"
        "2. Understand various Singlish spelling variations (e.g., 'mokakda', 'mkkd', 'moka d' all mean 'what').\n"
        "3. Always respond in natural, grammatically correct Sinhala Unicode.\n"
        "4. Be friendly and helpful, like a local Sri Lankan friend.\n"
        "5. If the input is in English, reply in Sinhala unless asked otherwise."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5 # Singlish වල තේරුම හොඳින් අනුමාන කිරීමට 0.5 සුදුසුයි
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, දත්ත ලබා ගැනීමේදී ගැටලුවක් මතු විය. නැවත උත්සාහ කරන්න."

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

if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

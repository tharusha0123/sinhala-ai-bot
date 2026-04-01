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
    
    # ව්‍යාකරණ සහ වචන (කුමක්ද/මොකක්ද) නිවැරදි කිරීමට දෙන දැඩි උපදෙස්
    system_instruction = (
        "You are a professional Sinhala AI assistant. "
        "Strictly follow these linguistic rules:\n"
        "1. Understand both formal Sinhala (e.g., කුමක්ද) and spoken Sinhala (e.g., මොකක්ද) as the same meaning.\n"
        "2. Respond in natural, grammatically correct Sinhala Unicode.\n"
        "3. Use a consistent style. If the user is informal, you can be friendly but keep the grammar perfect.\n"
        "4. Never translate literally from English; use Sinhala idioms and natural flow.\n"
        "5. Support Singlish input and convert it to accurate Sinhala context internally before answering."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.3 # වඩාත් නිවැරදි වචන තෝරා ගැනීමට temperature එක තවත් අඩු කළා
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

if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

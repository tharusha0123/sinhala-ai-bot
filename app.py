import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ ඇත්තම Groq API Key එක ඇතුළත් කරන්න
GROQ_API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional Sinhala AI assistant. Respond in natural, accurate Sinhala Unicode. Understand Singlish perfectly."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.6
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except:
        return "දත්ත ලබා ගැනීමේදී දෝෂයක් සිදු විය. කරුණාකර නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN (අති නවීන පෙනුම) ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖", layout="centered")

# CSS මගින් පෙනුම වෙනස් කිරීම
st.markdown("""
    <style>
    /* මුළු පිටුවේම පසුබිම */
    .stApp {
        background-color: #0e1117;
    }
    
    /* ප්‍රධාන මාතෘකාව (Title) */
    .main-title {
        font-size: 55px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00d4ff, #0055ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -50px;
        margin-bottom: 5px;
        font-family: 'Arial Black', sans-serif;
    }
    
    /* නිර්මාණය කළ අයගේ නම (Created By) */
    .footer {
        text-align: center;
        font-size: 16px;
        color: #8892b0;
        font-style: italic;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    /* Chat Messages ලස්සන කිරීම */
    .stChatMessage {
        border: 1px solid #1e293b;
        border-radius: 20px !important;
        background-color: #1a202c !important;
        margin-bottom: 15px;
    }
    
    /* Chat Input Bar එකේ පෙනුම */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# පෙනුම ප්‍රදර්ශනය කිරීම
st.markdown("<h1 class='main-title'>Sinhala AI Pro</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් ඕනෑම දෙයක් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

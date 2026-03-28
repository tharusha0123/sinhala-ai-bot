import streamlit as st
import requests
import json

# --- 1. CONFIGURATION ---
# ඔයා Google AI Studio එකෙන් ගත්ත අලුත්ම API Key එක මෙතනට දාන්න
API_KEY = "AIzaSyBd00qhYiGwd54skNsFpP30KL4U4Alc1yw"

def get_gemini_response(user_input):
    # මේ URL එක 100% ක් නිවැරදියි (v1 පාවිච්චි කර ඇත)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    # Singlish තේරුම් ගන්න සහ නිවැරදි සිංහලෙන් පිළිතුරු දීමට උපදෙස් (System Instruction)
    system_instruction = (
        "You are a professional Sinhala AI assistant created by Tharusha Rathnayake. "
        "The user might type in Singlish (Sinhala words in English letters, e.g., 'kohomada', 'usa gaha mokakda'). "
        "First, understand the meaning of the input. Then, always respond in clear, natural, and factual Sinhala Unicode. "
        "Be very precise and accurate with facts."
    )
    
    data = {
        "contents": [{
            "parts": [{"text": f"{system_instruction}\n\nUser Input: {user_input}"}]
        }],
        "generationConfig": {
            "temperature": 0.1,  # නිරවද්‍යතාවය වැඩි කිරීමට
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            # ලැබෙන පිළිතුර නිවැරදිව ලබා ගැනීම
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error: {response.status_code}. API Key එකේ හෝ සම්බන්ධතාවයේ දෝෂයකි."
    except Exception as e:
        return f"සම්බන්ධතාවයේ ගැටලුවකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Google Gemini 1.5 Flash තාක්ෂණයෙන් ක්‍රියාත්මක වේ | Created by Tharusha")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("පිළිතුර සකසමින්..."):
            answer = get_gemini_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

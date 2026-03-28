import streamlit as st
import requests
import json

# --- 1. CONFIGURATION ---
# ඔයාගේ API Key එක මෙතනට හරියටම දාන්න
API_KEY = "AIzaSyCyLmIbX0NJK1auohCc0VCEy5EhAYk3j_Y"

def get_gemini_response(user_input):
    # මේ URL එක 100% ක් ස්ථාවරයි
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [{
            "parts": [{"text": f"Respond in Sinhala language clearly: {user_input}"}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        # Error එකක් ආවොත් ඒක පෙන්වනවා
        return f"පද්ධතියේ දෝෂයක්: {response.status_code}. කරුණාකර API Key එක පරීක්ෂා කරන්න."

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI", page_icon="🤖")
st.title("සිංහල AI සහායකයා 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("මොනවද දැනගන්න ඕනේ?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("පිළිතුර සකසමින්..."):
            answer = get_gemini_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

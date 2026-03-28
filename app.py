import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# ඔයාගේ API Key එක මෙතනට දාන්න
API_KEY = "AIzaSyCK1KkU10SWy1yKBVxlwd-SLE4xkbcvmUU"

genai.configure(api_key=API_KEY)
# මේක අලුතින් එකතු කරන්න
import os
os.environ["GOOGLE_API_KEY"] = API_KEY
# පරණ එක වෙනුවට මේක දාන්න (models/ කියන කෑල්ල වැදගත්)
model = genai.GenerativeModel('models/gemini-pro')

# --- UI ---
st.set_page_config(page_title="Sinhala AI", page_icon="🤖")
st.title("සිංහල AI සහායකයා 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("මොනවද දැනගන්න ඕනේ?"):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        response = model.generate_content(f"Respond in Sinhala: {prompt}")
        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

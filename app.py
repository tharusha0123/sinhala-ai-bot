import streamlit as st
import requests

# --- CONFIGURATION ---
# ඔයා අලුතින් ගත්ත Groq API Key එක මෙතනට දාන්න
GROQ_API_KEY = "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"

def get_groq_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Always respond in Sinhala language clearly."},
            {"role": "user", "content": user_input}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# --- UI SETUP ---
st.set_page_config(page_title="Sinhala AI Assistant", page_icon="🤖")
st.title("සිංහල AI සහායකයා (Groq) 🤖")

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
        with st.spinner("සිතමින් පවතී..."):
            answer = get_groq_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

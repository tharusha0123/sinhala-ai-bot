import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයා අලුතින් ගත්ත Mistral API Key එක මෙතනට දාන්න
API_KEY = "jtvo27GCpDPRPsNTFrFBmc6i2jrgl73g"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-large-latest", # සිංහල සඳහා ඉතාම නිවැරදි model එක
        "messages": [
            {
                "role": "system", 
                "content": "You are a highly accurate Sinhala AI created by Tharusha. Understand Singlish and Sinhala perfectly. Always provide factual, grammatically correct, and natural Sinhala responses. If asked for size/area, provide the exact measurement in sq km."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}. API Key එක පරීක්ෂා කරන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ ගැටලුවකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("High Accuracy Free Mode | Created by Tharusha")

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
        with st.spinner("නිවැරදි පිළිතුර සොයමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

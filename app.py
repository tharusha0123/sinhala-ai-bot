import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ GROQ API Key එක මෙතනට දාන්න
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # සිංහල භාෂාව ඉතාම නිවැරදිව පාවිච්චි කරන්න කියලා AI එකට තදින්ම උපදෙස් දෙනවා
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "You are a highly intelligent and accurate Sinhala AI assistant. Your task is to understand the user's question in Sinhala and provide a factual, accurate answer in natural-sounding Sinhala. Focus strictly on answering the user's specific question correctly."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1,  # මේක 0.1 ට අඩු කිරීමෙන් AI එක බොරු කීම (Hallucination) සම්පූර්ණයෙන්ම වගේ නවතිනවා
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"දෝෂයකි: {response.status_code}"
    except Exception as e:
        return f"සම්බන්ධතාවයේ ගැටලුවකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    </style>
    """, unsafe_allow_html=True)

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Created by Tharusha Rathnayake")

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
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

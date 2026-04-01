import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Apilage API Key එක මෙතනට ලබා දෙන්න
APILAGE_API_KEY = "apk_f6c42e5eb8e57c987163218f9845413b55303f7e46f869e3"

def get_apilage_response(user_input):
    # නිවැරදි ලිපිනය (Endpoint URL)
    url = "https://api.apilageai.lk/v1/chat/completions" 
    
    headers = {
        "Authorization": f"Bearer {APILAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "apilage-1", # හෝ ඔවුන්ගේ dashboard එකේ ඇති model name එක
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional Sinhala AI. Answer accurately in natural Sinhala."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.3
    }
    
    try:
        # Timeout එකක් එකතු කිරීමෙන් හිරවීම වළක්වා ගත හැක
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status() 
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"දත්ත ලබා ගැනීමට නොහැකි විය. කරුණාකර ඔබගේ API Key එක සහ අන්තර්ජාලය පරීක්ෂා කරන්න."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🇱🇰")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("ප්‍රශ්නය මෙතන ලියන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_apilage_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

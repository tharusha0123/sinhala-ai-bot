import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = "q88gQmmMVBs5txpq0qT8BskYAZ2mnpvl"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # සිංග්ලිෂ් වචන සහ දත්ත 100% නිවැරදිව හඳුනා ගැනීමට දෙන උපදෙස්
    system_instruction = (
        "You are a factual Sinhala AI expert. Use this logic for Singlish:\n"
        "1. 'usa' = Height/Altitude (පිදුරුතලාගල = 2524m).\n"
        "2. 'wishalathwaya' = Area/Size (වර්ග කිලෝමීටර් 65,610).\n"
        "3. 'palala' = Width (උපරිම පළල = 240km).\n"
        "4. 'diga' = Length (උපරිම දිග = 435km).\n\n"
        "Always provide the exact measurement in natural Sinhala. Be very precise."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0 
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "තොරතුරු ලබා ගැනීමේ දෝෂයකි."

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🚀")

# Custom CSS
st.markdown("""
    <style>
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා 🤖</h1>", unsafe_allow_html=True)
st.write("---")

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
        with st.spinner("තොරතුරු සොයමින් පවතී..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

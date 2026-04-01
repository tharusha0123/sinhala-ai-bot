import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Apilage API Key එක මෙතනට ලබා දෙන්න
# (සාමාන්‍යයෙන් මේක apilage.io dashboard එකෙන් ගන්න පුළුවන්)
APILAGE_API_KEY = "apk_f6c42e5eb8e57c987163218f9845413b55303f7e46f869e3"

def get_apilage_response(user_input):
    url = "https://api.apilage.io/v1/chat/completions" # Apilage Endpoint එක
    
    headers = {
        "Authorization": f"Bearer {APILAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Apilage වල සිංහල හැකියාව උපරිම කිරීමට සකස් කළ Prompt එක
    data = {
        "model": "apilage-1", # හෝ dashboard එකේ සඳහන් model එක
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful and accurate Sinhala AI assistant. Provide answers in natural Sinhala Unicode."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Error එකක් ආවොත් අඳුනා ගැනීමට
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"දත්ත ලබා ගැනීමට නොහැකි විය: {str(e)}"

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI (Apilage)", page_icon="🇱🇰")

# සරල සහ ලස්සන Styling
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 2.2rem; color: #ffcc00; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා (Apilage)</h1>", unsafe_allow_html=True)
st.write("---")

# Chat History පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_apilage_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

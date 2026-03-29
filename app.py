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
    
    # සිංග්ලිෂ් වචන පටලවා නොගන්නා ලෙස දෙන ඉතාමත් ප්‍රබල උපදෙස් මාලාව
    system_instruction = (
        "You are an expert Sinhala/Singlish interpreter. Your task is to extract the correct intent from Singlish words.\n"
        "STRICT DEFINITIONS:\n"
        "- 'usa' = Height / Altitude (උස). Example: 'Lankawe usa' means 'How high is Sri Lanka'.\n"
        "- 'wishalathwaya' = Area / Size (වර්ග ප්‍රමාණය).\n"
        "- 'USA' (Capital letters) = United States of America.\n\n"
        "LOGIC STEP:\n"
        "1. Identify if the user is asking about a physical measurement (height/area) or a country.\n"
        "2. If the user asks 'lankawe usa', provide the height of Pidurutalagala in meters.\n"
        "3. Always answer in clear, formal Sinhala Unicode.\n"
        "4. Be factually 100% correct."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Analyze this Singlish query and answer accurately in Sinhala: {user_input}"}
        ],
        "temperature": 0.0 # වැරදි අර්ථකථන දීම වැළැක්වීමට 0.0 ම තබන්න
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, තොරතුරු ලබා ගැනීමේදී දෝෂයක් සිදු විය."

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🚀")

st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #00d4ff;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("තොරතුරු සොයමින් පවතී..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

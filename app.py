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
    
    # සිංග්ලිෂ් සහ සිංහල අතර ඇති සියලුම සමානකම් AI එකට හඳුන්වා දීම
    system_instruction = (
        "You are a specialized linguistic engine for Sinhala and Singlish. "
        "Your goal is to interpret Singlish terms accurately before answering.\n\n"
        
        "DICTIONARY RULES (Singlish to Sinhala Meaning):\n"
        "1. 'usa' / 'ussa' / 'height' = උස (Height/Altitude). "
        "   - If 'lankawe usa', refer to Pidurutalagala (2524m).\n"
        "2. 'palala' / 'width' = පළල (Width). "
        "   - If 'lankawe palala', refer to max width (240km).\n"
        "3. 'diga' / 'length' = දිග (Length). "
        "   - If 'lankawe diga', refer to max length (435km).\n"
        "4. 'wishalathwaya' / 'size' / 'area' = වර්ග ප්‍රමාණය (Area). "
        "   - If 'lankawe wishalathwaya', refer to 65,610 sq km.\n"
        "5. 'bara' / 'weight' = බර (Weight).\n"
        "6. 'USA' (All Caps) = United States of America.\n\n"
        
        "LOGIC STEPS:\n"
        "- Step 1: Check if the word is 'usa' (height) or 'USA' (country).\n"
        "- Step 2: Extract the correct factual data in English.\n"
        "- Step 3: Provide a professional answer in Sinhala Unicode.\n"
        "- Step 4: Be precise with numbers and units (m, km, sq km)."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Think carefully about the intent and answer: {user_input}"}
        ],
        "temperature": 0.0 # වැරදි අර්ථකථන සම්පූර්ණයෙන්ම නැවැත්වීමට
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, සම්බන්ධතාවයේ දෝෂයක්. කරුණාකර නැවත උත්සාහ කරන්න."

# --- 2. UI SETTINGS ---
st.set_page_config(page_title="Sinhala AI Assistant", page_icon="🤖")

st.markdown("""
    <style>
    .main-title { font-size: 2.8rem; color: #00d4ff; text-align: center; font-weight: 800; }
    .stChatMessage { border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා 🤖</h1>", unsafe_allow_html=True)
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

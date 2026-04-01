import streamlit as st
import requests

# --- 1. CONFIGURATION & API ---
# API Key එක Streamlit Secrets වලින් ලබා ගැනීම (Security සඳහා)
# නැත්නම් කෙලින්ම මෙතනට "MISTRAL_API_KEY" එක දාන්නත් පුළුවන්.
MISTRAL_API_KEY = st.secrets.get("MISTRAL_API_KEY", "QcwdNlmfqQulxAbH9HAucYtt1AW5VePj")

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {
                "role": "system", 
                "content": "You are a precise Sinhala AI. Translate user input to English, find the fact, and answer in natural Sinhala. Max 1 sentence."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Error එකක් ආවොත් කෙලින්ම exception එකට යයි
        return response.json()['choices'][0]['message']['content']
    except Exception:
        return "කණගාටුයි, දත්ත ලබා ගැනීමට නොහැකි විය. කරුණාකර නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI", page_icon="🤖")

# සරල Styling
st.markdown("<h1 style='text-align: center; color: #00d4ff;'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.divider()

# Chat History එක තබා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ Chat ප්‍රදර්ශනය කිරීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input එක ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    # User message එක පෙන්වීම
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        with st.spinner("සිතමින් පවතී..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

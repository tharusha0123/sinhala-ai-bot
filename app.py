import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Mistral API Key එක මෙතනට දාන්න
API_KEY = "q88gQmmMVBs5txpq0qT8BskYAZ2mnpvl"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # පියවරෙන් පියවර නිවැරදිව හිතන්න කියලා AI එකට දෙන උපදෙස් (System Prompt)
    system_instruction = (
        "You are a professional Sinhala AI assistant. Follow these strict rules:\n"
        "1. Context logic: 'usa' always means Height (උස). 'wishalathwaya' always means Area (වර්ග ප්‍රමාණය).\n"
        "2. Factual thinking: First find the correct data in English (e.g., Height of Pidurutalagala is 2524m).\n"
        "3. Final Output: Translate the correct data into natural, formal Sinhala Unicode.\n"
        "4. Be brief and highly accurate. If you don't know, say 'මම ඒ ගැන නොදනී'."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1 # Accuracy එක වැඩි කිරීමට
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code}. ප්ලෑන් එකක් තෝරා ඇත්දැයි බලන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Mistral Large - High Accuracy Mode | Created by Tharusha")

# Chat history එක පවත්වාගෙන යාම
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input එක ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("නිවැරදි තොරතුරු සොයමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

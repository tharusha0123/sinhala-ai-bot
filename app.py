import streamlit as st
import requests
import json

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ API Key එක දාන්න
API_KEY = "AIzaSyBd00qhYiGwd54skNsFpP30KL4U4Alc1yw"

def get_gemini_response(user_input):
    # මම මෙතන URL එක 100% නිවැරදිව හදලා තියෙන්නේ
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [{
            "parts": [{"text": f"You are a helpful Sinhala AI assistant. Respond in natural Sinhala: {user_input}"}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    try:
        # මෙතනදී කෙලින්ම URL එකට පණිවිඩය යවනවා
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error {response.status_code}: API Key එක හෝ URL එක වැරදියි. කරුණාකර පරීක්ෂා කරන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

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
            answer = get_gemini_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

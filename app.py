import streamlit as st
import requests
import json

# --- 1. CONFIGURATION ---
# ඔයා අලුතින් ගත්ත Gemini API Key එක මෙතනට දාන්න
API_KEY = "AIzaSyDSllOH_riZzyidocOnmpSPOvHVv3kO_oQ"

def get_gemini_response(user_input):
    # Gemini 1.5 Flash API URL
    # v1beta වෙනුවට v1 දාලා බලන්න
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"    
    headers = {'Content-Type': 'application/json'}
    
    # AI එකට දෙන විශේෂ උපදෙස් (System Instruction)
    system_prompt = "ඔබ තාරුෂ (Tharusha) විසින් නිර්මාණය කරන ලද සිංහල AI සහායකයෙකි. ඔබ සැමවිටම ඉතා නිවැරදි ව්‍යාකරණ සහිතව සිංහල භාෂාවෙන් පමණක් පිළිතුරු දිය යුතුය. ඉතා සුහදශීලී වන්න."
    
    data = {
        "contents": [{
            "parts": [{"text": f"{system_prompt}\n\nUser: {user_input}"}]
        }]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return "කණගාටුයි, සම්බන්ධතාවයේ දෝෂයක් පවතී. කරුණාකර API Key එක පරීක්ෂා කරන්න."

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

# වෙබ් අඩවියේ පෙනුම ලස්සන කිරීම
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input { color: #ffffff; }
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
            answer = get_gemini_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

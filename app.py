import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# මෙතන තියෙන 'gsk_...' වෙනුවට ඔයාගේ ඇත්තම Groq API Key එක දාන්න
GROQ_API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional Sinhala AI assistant. The user will ask in Sinhala or Singlish. Always respond in natural, accurate Sinhala Unicode. Be friendly and helpful."
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.5
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}. API Key එක හෝ Model එක පරීක්ෂා කරන්න."
    except Exception as e:
        return f"දත්ත ලබා ගැනීමට නොහැකි විය: {str(e)}"

# --- 2. UI DESIGN (අතුරුමුහුණත) ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖")

# වෙබ් අඩවියේ පෙනුම ලස්සන කිරීමට CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .title { font-size: 35px; font-weight: bold; color: #00d4ff; text-align: center; }
    .stChatMessage { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<p class='title'>සිංහල AI සහායකයා 🤖</p>", unsafe_allow_html=True)
st.write("---")

# Chat History පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නය ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    # User මැසේජ් එක පෙන්වීම
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("පිළිතුර සකසමින්..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

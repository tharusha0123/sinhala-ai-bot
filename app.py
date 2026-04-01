import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Mistral API Key එක මෙතන තියෙනවා
MISTRAL_API_KEY = "QcwdNlmfqQulxAbH9HAucYtt1AW5VePj"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 🔴 සිංහල සහ Singlish නිවැරදිව තේරුම් ගැනීමට ලබා දෙන විශේෂ උපදෙස්
    system_instruction = (
        "You are a highly accurate Sinhala AI. To ensure 100% accuracy, follow these steps:\n"
        "1. Translate the user's Singlish/Sinhala input into English mentally.\n"
        "2. Find the correct world fact for that English question.\n"
        "3. Translate that fact into perfect, natural Sinhala Unicode.\n"
        "4. Context rules: 'usa'=height, 'diga'=length, 'palala'=width, 'rata'=country, 'podima'=smallest, 'lokuma'=largest.\n"
        "5. Direct answer only. 1 sentence max."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Think in English, answer in Sinhala: {user_input}"}
        ],
        "temperature": 0.0 # වැරදීමේ සම්භාවිතාව අවම කිරීමට
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "දත්ත ලබා ගැනීමට නොහැකි විය."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖")

# Interface එක ලස්සන කිරීමට යොදාගත් CSS
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    .stChatMessage { border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

# Chat History එක පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නය ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    # User මැසේජ් එක පෙන්වීම
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("තොරතුරු සොයමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

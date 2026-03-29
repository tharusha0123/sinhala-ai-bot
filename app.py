import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = "I8LgRmMLn3brmAO2qLPQquZtsDRdBLaw"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "You are a strictly factual Sinhala AI. Rules:\n"
        "1. Direct answer only (1-2 sentences).\n"
        "2. No thinking process or analysis.\n"
        "3. Interpret Singlish: 'usa'=height, 'diga'=length, 'palala'=width, 'duupath'=islands, 'gaga'=river.\n"
        "4. Fact Check: Sweden has the most islands (267,000+). Do not hallucinate."
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
        return "දත්ත ලබා ගැනීමේ දෝෂයකි."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stChatMessage { background: rgba(255, 255, 255, 0.05) !important; backdrop-filter: blur(10px); border-radius: 15px !important; }
    .main-title { font-size: 3rem; font-weight: 800; text-align: center; background: linear-gradient(to right, #00d4ff, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff;'>🚀 AI Panel</h2>", unsafe_allow_html=True)
    st.write("---")
    st.success("Mode: Ultra-Accuracy ✅")
    st.write(f"**Developer:** Tharusha Rathnayake")

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages (මෙතන පේළි ටික මම හරියටම හැදුවා)
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
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

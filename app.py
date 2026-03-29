import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = "q88gQmmMVBs5txpq0qT8BskYAZ2mnpvl"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": "You are a factual Sinhala AI. Context: 'usa'=Height, 'wishalathwaya'=Area. Answer in formal Sinhala."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "දත්ත ලබා ගැනීමේ දෝෂයකි."

# --- 2. UI ENHANCEMENTS (ADVANCED CSS) ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    /* Sidebar Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    /* Chat Bubble Styling */
    .stChatMessage {
        background-color: #1e1e1e !important;
        border: 1px solid #333;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    /* Title Styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#00d4ff, #005f73);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & QUICK BUTTONS ---
with st.sidebar:
    st.markdown("## ⚙️ AI Control Panel")
    st.write("---")
    st.info("Presenting: **Sinhala Intelligence v2.0**")
    
    st.markdown("### ⚡ Quick Queries")
    # Quick buttons for presentation ease
    if st.button("🗺️ USA වර්ග ප්‍රමාණය?"):
        st.session_state.quick_query = "USA wishalathwaya kiyada?"
    if st.button("⛰️ ලංකාවේ උසම තැන?"):
        st.session_state.quick_query = "lankawe usa kiyada?"
    
    st.write("---")
    st.markdown("**Developer:** Tharusha Rathnayake")

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Logic to handle Quick Buttons
prompt = st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න...")
if st.session_state.get('quick_query'):
    prompt = st.session_state.quick_query
    del st.session_state.quick_query

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("තොරතුරු සොයමින් පවතී..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

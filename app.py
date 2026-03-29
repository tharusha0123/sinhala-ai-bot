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
    
    system_instruction = (
        "You are a professional Sinhala AI assistant. Follow these strict rules:\n"
        "1. Context logic: 'usa' always means Height (උස). 'wishalathwaya' always means Area (වර්ග ප්‍රමාණය).\n"
        "2. Factual thinking: First find the correct data in English.\n"
        "3. Final Output: Translate the correct data into natural, formal Sinhala Unicode.\n"
        "4. Be brief and highly accurate."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "දත්ත ලබා ගැනීමේ දෝෂයකි. කරුණාකර නැවත උත්සාහ කරන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයකි: {e}"

# --- 2. UI SETTINGS (LASSANA KIRIMA) ---
st.set_page_config(page_title="Sinhala AI Assistant", page_icon="🤖", layout="centered")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    h1 {
        color: #00d4ff;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .status-text {
        color: #888;
        font-size: 0.9rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("AI Settings")
    st.info("මෙම AI සහායකයා සිංහල සහ Singlish යන භාෂා දෙකම නිවැරදිව හඳුනා ගනී.")
    st.write("---")
    st.write("**Created by:** Tharusha Rathnayake")
    st.success("Mode: Ultra-Accuracy ✅")

# Main Title
st.markdown("<h1>සිංහල AI සහායකයා 🤖</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-text'>Mistral Large 2 | High Accuracy Sinhala Mode</p>", unsafe_allow_html=True)
st.write("---")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("නිවැරදි තොරතුරු පරීක්ෂා කරමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

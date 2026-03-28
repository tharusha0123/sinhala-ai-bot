import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# ඔයාගේ Gemini API Key එක මෙතනට දාන්න
API_KEY = "AIzaSyBd00qhYiGwd54skNsFpP30KL4U4Alc1yw"

# Google Gemini Setup
genai.configure(api_key=API_KEY)

# AI එකට දෙන උපදෙස් (System Instruction)
instruction = (
    "You are a professional Sinhala AI assistant created by Tharusha Rathnayake. "
    "The user will often type in Singlish (e.g., 'kohomada', 'usa gaha mokakda'). "
    "Always understand the Singlish meaning and reply in clear, accurate, and natural Sinhala Unicode. "
    "If someone asks who you are, say you are 'Tharusha's Sinhala AI'."
)

# Model එක ලෑස්ති කිරීම
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Google Gemini 1.5 Flash (Official) | Created by Tharusha")

if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input එක ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            # පිළිතුර ලබා ගැනීම
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")

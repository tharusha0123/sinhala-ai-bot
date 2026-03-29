import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# ඔයාගේ අලුත් Gemini API Key එක මෙතනට දාන්න
API_KEY = "AIzaSyDpAOu9JZJjkMRK3mDaF6uYpGw3Ur7WUjA"

genai.configure(api_key=API_KEY)

# AI එකට දෙන ලොජික් එක (System Instruction)
instruction = (
    "You are a professional Sinhala AI assistant created by Tharusha Rathnayake. "
    "Your goal is 100% factual accuracy. Follow these rules:\n"
    "1. Understand Singlish intent: 'usa' = Height (උස), 'wishalathwaya' = Area/Size (වර්ග ප්‍රමාණය).\n"
    "2. If asked 'lankawe usa', provide the height of Pidurutalagala (2524m).\n"
    "3. If asked 'USA wishalathwaya', provide the area of the country USA (9.8 million sq km).\n"
    "4. Always reply in natural, perfect Sinhala Unicode.\n"
    "5. Do not hallucinate. If you don't know, say you don't know."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Google Gemini 1.5 Flash | High Accuracy Mode")

if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ මැසේජ් පෙන්වීම
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
            # නිරවද්‍යතාවය වැඩි කිරීමට temperature එක 0.1 ලෙස තබා ඇත
            response = model.generate_content(
                prompt, 
                generation_config=genai.types.GenerationConfig(temperature=0.1)
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")

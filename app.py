import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# මෙතනට ඔයාගේ Groq API Key එක ඇතුළත් කරන්න
GROQ_API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.apilageai.lk/v1/chat/completions" # නැත්නම් Groq URL එක පාවිච්චි කරන්න
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # සිංහල ව්‍යාකරණ නිවැරදි කිරීමට ලබා දෙන දැඩි උපදෙස්
    system_instruction = (
        "You are a professional Sinhala AI assistant with perfect grammar skills. "
        "Strictly follow these rules for Sinhala responses:\n"
        "1. Use natural Sinhala sentence structures (SOV - Subject-Object-Verb).\n"
        "2. Ensure proper subject-verb agreement (උක්ත-ආඛ්‍යාත ගැලපීම).\n"
        "3. Use spoken-style Sinhala (කථන භාෂාව) for a friendly vibe, but keep it grammatically correct.\n"
        "4. Avoid direct word-for-word translations from English.\n"
        "5. If the user asks in Singlish, understand the intent and reply in perfect Sinhala Unicode.\n"
        "6. Do not mix formal and informal Sinhala in the same sentence."
    )
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.4 # ව්‍යාකරණ වැරදීම් අවම කිරීමට temperature එක අඩු කළා
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        return response.json()['choices'][0]['message']['content']
    except:
        return "කණගාටුයි, පිළිතුර ලබා ගැනීමේදී ගැටලුවක් මතු විය. නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="සිංහල Chat Bot", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .main-title {
        font-size: 50px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00d4ff, #0055ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: -50px;
        margin-bottom: 5px;
    }
    .footer {
        text-align: center;
        font-size: 15px;
        color: #8892b0;
        font-style: italic;
        margin-bottom: 30px;
    }
    .stChatMessage { border-radius: 15px !important; background-color: #1a202c !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල Chat Bot</h1>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Created by Tharusha Rathnayake</p>", unsafe_allow_html=True)
st.write("---")

# --- 3. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("පිළිතුර සකසමින්..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Mistral API Key එක මෙතනට දාන්න
MISTRAL_API_KEY = "I8LgRmMLn3brmAO2qLPQquZtsDRdBLaw"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # AI එකට බොරු කීම වැළැක්වීමට සහ නිවැරදි සිංහල ලබාදීමට දෙන උපදෙස්
    system_instruction = (
        "You are a strictly factual Sinhala AI assistant. Follow these absolute rules:\n"
        "1. FACTUALITY: Only provide real-world facts. If unsure, say 'මම ඒ ගැන නොදනිමි'.\n"
        "2. NO HALLUCINATION: Never invent names like 'Asēriya'. Verify facts (e.g., Sweden has the most islands).\n"
        "3. GRAMMAR: Use natural, formal Sinhala. (e.g., 'ලෝකයේ වැඩිම දූපත් ඇති රට ස්වීඩනයයි.')\n"
        "4. SINGLISH MAPPING: 'usa'=height, 'diga'=length, 'palala'=width, 'duupath'=islands, 'rata'=country, 'gaga'=river.\n"
        "5. OUTPUT: Direct answer only. 1-2 sentences maximum. No analysis steps."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Answer this factual query accurately in Sinhala: {user_input}"}
        ],
        "temperature": 0.0 # වැරදි අර්ථකථන සම්පූර්ණයෙන්ම නැවැත්වීමට මෙය 0.0 ම තබන්න
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "දෝෂයකි: API සම්බන්ධතාවය පරීක්ෂා කරන්න."
    except:
        return "සම්බන්ධතාවයේ දෝෂයකි."

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

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["

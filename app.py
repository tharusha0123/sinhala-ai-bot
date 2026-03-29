import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = "I8LgRmMLn3brmAO2qLPQquZtsDRdBLaw"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # මේ තමයි රහස - අපි දත්ත ටික AI එකට කලින්ම දෙනවා (Knowledge Base)
    knowledge_base = """
    FACTS TO USE:
    - Sri Lanka Highest Point: Pidurutalagala (2524m).
    - Sri Lanka Max Width: 240km.
    - Sri Lanka Max Length: 435km.
    - Sri Lanka Area: 65,610 sq km.
    - World's Most Islands: Sweden (over 267,000 islands).
    - World's Longest River: Nile (6,650km).
    - Singlish Mapping: 'usa'=height, 'palala'=width, 'diga'=length, 'duupath'=islands, 'gaga'=river.
    """
    
    system_instruction = (
        f"{knowledge_base}\n"
        "You are a professional factual AI. Rules:\n"
        "1. Use the facts provided above ONLY. Do not invent facts.\n"
        "2. Answer in perfect, formal Sinhala. (No 'Asēriya' or weird words).\n"
        "3. If 'lankawe usa' is asked, answer about Pidurutalagala.\n"
        "4. If 'duupath' is asked, answer about Sweden.\n"
        "5. Direct 1-sentence answer only."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0 # Very important for accuracy
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "දත්ත ලබා ගැනීමේ දෝෂයකි."

# --- 2. UI DESIGN (PROFESSIONAL) ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63); color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🚀 Control Center")
    st.info("Verified High-Accuracy Mode")
    st.write(f"Developer: Tharusha")

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා</h1>", unsafe_allow_html=True)
st.write("---")

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
        with st.spinner("තොරතුරු සොයමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

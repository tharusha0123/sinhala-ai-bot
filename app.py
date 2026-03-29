import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = "I8LgRmMLn3brmAO2qLPQquZtsDRdBLaw"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
    
    # සිංග්ලිෂ් වචන වල තේරුම සහ දත්ත නිවැරදිව හඳුනා ගැනීමට දෙන නවතම උපදෙස්
    system_instruction = (
        "You are a professional factual AI assistant. Rules:\n"
        "1. Understand Singlish intent: 'usa'=height, 'diga'=length, 'palala'=width, 'lokuma rata'=largest country, 'duupath'=islands.\n"
        "2. First, identify the core question. (e.g., if asked about 'lokuma rata', it's Russia).\n"
        "3. Provide the answer in natural, grammatically correct Sinhala Unicode.\n"
        "4. Keep the answer direct and short (1-2 sentences).\n"
        "5. Example: 'lokaye lokuma rata mokakd' -> 'ලෝකයේ විශාලතම රට රුසියාවයි.'\n"
        "6. If asked about Sri Lanka's measurements: Height=2524m, Width=240km, Length=435km."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1 # නිවැරදි බව සහ නම්‍යශීලී බව අතර සමබරතාවයක් සඳහා
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "API සම්බන්ධතාවයේ දෝෂයකි."
    except:
        return "දත්ත ලබා ගැනීමට නොහැකි විය."

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63); color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    .stChatMessage { background: rgba(255, 255, 255, 0.05) !important; border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

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

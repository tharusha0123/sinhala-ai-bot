import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Mistral API Key එක (console.mistral.ai එකෙන් ගත්තු එක) මෙතනට දාන්න
MISTRAL_API_KEY = "q88gQmmMVBs5txpq0qT8BskYAZ2mnpvl"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # ඉතාමත් ශක්තිමත් සිංග්ලිෂ් සහ සිංහල උපදෙස් මාලාව
    system_instruction = (
        "You are a factual Sinhala AI expert. Your goal is to provide DIRECT and NATURAL Sinhala answers.\n\n"
        "STRICT SINGLISH RULES:\n"
        "- 'usa' / 'ussa' = Height/Altitude (උස). If about Sri Lanka, answer 'Pidurutalagala is 2524m'.\n"
        "- 'palala' = Width (පළල). If about Sri Lanka, answer '240km'.\n"
        "- 'diga' = Length (දිග). If about Sri Lanka, answer '435km'.\n"
        "- 'wishalathwaya' = Area (වර්ග ප්‍රමාණය). If about Sri Lanka, answer '65,610 sq km'.\n"
        "- 'gaga' / 'gangawa' = River (ගංගාව).\n\n"
        "OUTPUT FORMAT:\n"
        "1. Do NOT show any thinking process or analysis like 'ප්‍රමාණ විශ්ලේෂණය'.\n"
        "2. Directly provide the answer in 1 or 2 natural Sinhala sentences.\n"
        "3. Use professional and natural Sinhala (e.g., use 'ගංගාවයි' or 'වේ' instead of 'ගඟ ය').\n"
        "4. Be 100% factually correct with numbers and units."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0 # වැරදි තොරතුරු දීම වැළැක්වීමට
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "කණගාටුයි, දත්ත ලබා ගැනීමේ දෝෂයක්. කරුණාකර API Key එක පරීක්ෂා කරන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයකි: {e}"

# --- 2. UI SETTINGS (LASSANA KIRIMA) ---
st.set_page_config(page_title="Sinhala AI Assistant", page_icon="🤖", layout="centered")

# Custom CSS for Professional UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    h1 { color: #00d4ff; text-align: center; font-weight: 800; }
    .status-tag { color: #888; text-align: center; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar with Presentation Info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("AI Control Panel")
    st.write("---")
    st.info("සිංහල සහ සිංග්ලිෂ් යන භාෂා දෙකම නිවැරදිව හඳුනාගැනීමට මෙම පද්ධතිය සමත් වේ.")
    st.write("**ප්‍රවර්ධක:** Tharusha Rathnayake")
    st.success("තත්ත්වය: සක්‍රීයයි ✅")

# Main Header
st.markdown("<h1>සිංහල AI සහායකයා 🤖</h1>", unsafe_allow_html=True)
st.markdown("<p class='status-tag'>Mistral Large 2 | High-Precision Mode</p>", unsafe_allow_html=True)
st.write("---")

# Chat History Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Logic
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("තොරතුරු සොයමින් පවතී..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

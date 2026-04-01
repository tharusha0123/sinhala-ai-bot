import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# ඔයාගේ Gemini API Key එක මෙතනට ලබා දෙන්න
GEMINI_API_KEY = "AIzaSyAhHLwj-hFgTC7jlCM0zMXIQ8z3vcwNl9I"

# Gemini Config කිරීම
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_input):
    # Model එක තෝරා ගැනීම (Gemini 1.5 Flash වඩාත් වේගවත්ය)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # AI එකට දෙන විශේෂ උපදෙස් (System Prompt)
    # මේකෙන් සිංහල භාෂාව වඩාත් නිවැරදිව ලබා දීමට AI එක පොළඹවනවා.
    system_instruction = (
        "You are a highly accurate Sinhala AI. To ensure 100% accuracy, follow these steps:\n"
        "1. Translate the user's Singlish/Sinhala input into English mentally.\n"
        "2. Find the correct world fact for that English question.\n"
        "3. Translate that fact into perfect, natural Sinhala Unicode.\n"
        "4. Context rules: 'usa'=height, 'diga'=length, 'palala'=width, 'rata'=country, 'podima'=smallest, 'lokuma'=largest.\n"
        "5. Direct answer only. 1 sentence max."
    )
    
    try:
        # Gemini හරහා පිළිතුර ලබා ගැනීම
        response = model.generate_content(f"{system_instruction}\n\nUser Question: {user_input}")
        return response.text
    except Exception as e:
        return f"දත්ත ලබා ගැනීමට නොහැකි විය: {str(e)}"

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro (Gemini)", page_icon="🤖")

# Interface එක ලස්සන කිරීමට CSS
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    .stChatMessage { border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා (Gemini)</h1>", unsafe_allow_html=True)
st.write("---")

# Chat History පවත්වා ගැනීම
if "messages" not in st.session_state:
    st.session_state.messages = []

# කලින් කළ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input ලබා ගැනීම
if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    # User message එක පෙන්වීම
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Gemini සිතමින් පවතී..."):
            answer = get_gemini_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

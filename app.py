import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURATION ---
# ඔයාගේ OpenAI API Key එක මෙතනට ලබා දෙන්න
OPENAI_API_KEY = "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"

# OpenAI Client එක සකස් කිරීම
client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(user_input):
    # සිංහල නිවැරදිව ලබා ගැනීමට වැඩිදියුණු කළ උපදෙස් (System Prompt)
    system_instruction = (
        "You are a highly accurate Sinhala AI. To ensure 100% accuracy, follow these steps:\n"
        "1. Translate the user's Singlish/Sinhala input into English mentally.\n"
        "2. Find the correct world fact for that English question.\n"
        "3. Translate that fact into perfect, natural Sinhala Unicode.\n"
        "4. Context rules: 'usa'=height, 'diga'=length, 'palala'=width, 'rata'=country, 'podima'=smallest, 'lokuma'=largest.\n"
        "5. Direct answer only. 1 sentence max."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # වේගවත් සහ ලාභදායී model එක
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"Think in English, answer in Sinhala: {user_input}"}
            ],
            temperature=0.0 # වැරදීමේ සම්භාවිතාව අවම කිරීමට
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"දත්ත ලබා ගැනීමට නොහැකි විය: {str(e)}"

# --- 2. UI DESIGN ---
st.set_page_config(page_title="Sinhala AI Pro (OpenAI)", page_icon="🤖")

# Interface එක ලස්සන කිරීමට CSS (Custom Styling)
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    .main-title { font-size: 2.5rem; color: #00d4ff; text-align: center; font-weight: bold; }
    .stChatMessage { border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>සිංහල AI සහායකයා (OpenAI)</h1>", unsafe_allow_html=True)
st.write("---")

# Chat History පවත්වා ගැනීම (Session State)
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
        with st.spinner("සිතමින් පවතී..."):
            answer = get_openai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

import streamlit as st
from groq import Groq

# API Key එක ලබා ගැනීම
GROQ_API_KEY = st.secrets.get("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")
client = Groq(api_key=GROQ_API_KEY)

def get_groq_response(user_input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional Sinhala AI assistant."},
                {"role": "user", "content": user_input},
            ],
            # අලුත්ම සහ ස්ථාවරම Model එක මෙන්න
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"දෝෂයක් සිදු විය: {str(e)}"

# UI කොටස
st.title("සිංහල AI (Groq)")
if prompt := st.chat_input("අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = get_groq_response(prompt)
        st.markdown(response)

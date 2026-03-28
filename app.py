import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ GROQ API Key එක (gsk_...) මෙතනට දාන්න
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # මෙතනදී අපි AI එකට කියනවා පියවරෙන් පියවර නිවැරදි පිළිතුර හදන්න කියලා
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": """You are an expert Sinhala Translator and AI Assistant. 
                Follow these steps for every user input:
                Step 1: If the input is in Singlish or Sinhala, understand its factual meaning.
                Step 2: Find the 100% correct factual answer to that question.
                Step 3: Translate that factual answer into formal, natural, and grammatically perfect Sinhala.
                Step 4: Only provide the final Sinhala answer. Do not give any English.
                Example: If asked 'lokaye usama gaha', answer 'ලෝකයේ උසම ගස වන්නේ හයිපීරියන් (Hyperion) නැමැති රෙඩ්වුඩ් ගසයි.'"""
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0, # Accuracy එක වැඩි කිරීමට
        "top_p": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "දෝෂයකි. කරුණාකර නැවත උත්සාහ කරන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI Assistant", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Advanced accuracy mode enabled | Created by Tharusha")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("සිංහලෙන් හෝ Singlish වලින් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("නිවැරදි පිළිතුර සකසමින්..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

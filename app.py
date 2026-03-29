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
    
    # සිංග්ලිෂ් සහ කරුණු නිවැරදිව ලබා ගැනීමට විශේෂ ප්‍රොම්ප්ට් එකක්
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": """You are a highly advanced Sinhala AI. 
                1. If the input is in Singlish (e.g. 'kohomada'), understand its meaning first.
                2. Think of the 100% correct factual answer in English.
                3. Translate that factual answer into natural, perfect Sinhala Unicode.
                4. Be very precise. If asked for 'size of USA', give the area in sq km.
                5. Do not hallucinate or give wrong info."""
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0, # මේක 0 නිසා බොරු කියන්නේ නැහැ
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return "කණගාටුයි, පද්ධතියේ දෝෂයක්. කරුණාකර නැවත උත්සාහ කරන්න."
    except Exception as e:
        return f"සම්බන්ධතාවයේ දෝෂයකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI Assistant", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Factual Accuracy Mode | Created by Tharusha Rathnayake")

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
        with st.spinner("නිවැරදි පිළිතුර සොයමින්..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ GROQ API Key එක මෙතනට දාන්න
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # සිංග්ලිෂ් (Singlish) තේරුම් ගැනීමට විශේෂ උපදෙස් මෙතන තියෙනවා
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": """You are an advanced Sinhala AI. 
                1. The user might type in 'Singlish' (Sinhala words using English letters, e.g., 'kohomada', 'usa gaha mokakda'). 
                2. Your first task is to understand the meaning of the Singlish text.
                3. Then, provide a highly accurate, factual answer in proper Sinhala Unicode (සිංහල අකුරින්).
                4. Be direct and precise. If the user asks for the tallest tree, answer 'Hyperion' or 'Redwood' in Sinhala."""
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0,
        "top_p": 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Connection Error: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Singlish සහ සිංහල අකුරු යන දෙකම තේරුම් ගත හැක.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Singlish වලින් හෝ සිංහලෙන් අසන්න..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("පණිවිඩය තේරුම් ගනිමින්..."):
            answer = get_ai_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

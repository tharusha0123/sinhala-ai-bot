import streamlit as st
import requests

# --- 1. CONFIGURATION ---
API_KEY = "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"

def get_ai_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prompt එක තවත් දියුණු කර ඇත
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": """You are an extremely accurate Sinhala AI Assistant.
                User input can be in Sinhala or Singlish.
                Strictly follow these rules:
                1. Translate the user input into English internally to understand the exact meaning.
                2. Find the precise factual answer in English.
                3. Translate that exact answer into natural, perfect Sinhala.
                4. Do not provide information that was not asked. If asked for 'size', provide 'size', not 'city'.
                5. Keep the response brief and accurate."""
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
            return "කණගාටුයි, සම්බන්ධතාවයේ ගැටලුවක්. නැවත උත්සාහ කරන්න."
    except Exception as e:
        return f"දෝෂයකි: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")

st.title("සිංහල AI සහායකයා 🤖")
st.caption("Factual Accuracy Mode Enabled | Created by Tharusha")

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

import streamlit as st
import requests

# --- 1. CONFIGURATION ---
# ඔයාගේ Mistral Key එක මෙතනට දාන්න
MISTRAL_API_KEY = "jtvo27GCpDPRPsNTFrFBmc6i2jrgl73g"

def get_mistral_response(user_input):
    url = "https://api.openai.com/v1/chat/completions" # Mistral can use OpenAI format sometimes, but standard is:
    url = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # මෙතන තමයි මැජික් එක තියෙන්නේ - Few-Shot Prompting
    system_message = (
        "You are a factual Sinhala AI. Your goal is 100% accuracy. "
        "Strictly follow these examples for logic:\n"
        "Example 1: User asks 'USA wishalathwaya' -> Understand as 'Area'. Answer: 'ඇමරිකා එක්සත් ජනපදයේ වර්ග ප්‍රමාණය වර්ග කිලෝමීටර් මිලියන 9.8 කි.'\n"
        "Example 2: User asks 'Usa gaha' -> Understand as 'Tallest tree'. Answer: 'ලෝකයේ උසම ගස වන්නේ හයිපීරියන් (Hyperion) නැමැති රෙඩ්වුඩ් ගසයි.'\n"
        "Rule: Always translate Singlish to English internally to find the fact, then translate back to perfect Sinhala. "
        "Do not confuse 'Size/Area' with 'Largest city' or 'Population'."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0 # වැරදි උත්තර දෙන එක නවත්තන්න මේක 0.0 ම තියන්න
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

# --- 2. UI SETUP ---
st.set_page_config(page_title="Sinhala AI by Tharusha", page_icon="🤖")
st.title("සිංහල AI සහායකයා 🤖")
st.caption("Ultra-Accuracy Mode Enabled")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("අසන්න..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("නිවැරදි තොරතුරු පරීක්ෂා කරමින්..."):
            answer = get_mistral_response(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

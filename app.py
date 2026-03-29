import streamlit as st
import requests

# --- 1. CONFIGURATION ---
MISTRAL_API_KEY = "q88gQmmMVBs5txpq0qT8BskYAZ2mnpvl"

def get_mistral_response(user_input):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Direct Answer Logic (Clean & Factually Correct)
    system_instruction = (
        "You are a factual Sinhala AI. Your goal is to provide DIRECT, SIMPLE, and NATURAL Sinhala answers.\n"
        "RULES:\n"
        "1. Do NOT show any analysis or thinking process.\n"
        "2. Directly answer in 1-2 sentences.\n"
        "3. Interpret Singlish: 'usa'=height, 'diga'=length, 'palala'=width, 'wishalathwaya'=area, 'gaga'=river.\n"
        "4. Use natural grammar like 'ලෝකයේ දිගම ගංගාව නයිල් ගංගාවයි' (ending with 'යි')."
    )
    
    data = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.0
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "දත්ත ලබා ගැනීමේ දෝෂයකි. නැවත උත්සාහ කරන්න."

# --- 2. UI DESIGN (ADVANCED CSS) ---
st.set_page_config(page_title="Sinhala AI Pro", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Glassmorphism Chat Bubbles */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 15px !important;
    }
    
    /* Title Styling */
    .main-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(to right, #00d4ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .sub-title {
        text-align: center;
        color: #aaa;
        font-size: 1rem;
        margin-bottom: 30px;
    }

    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4

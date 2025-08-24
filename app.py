import streamlit as st
from dotenv import load_dotenv
import os
import requests
from sarvamai import SarvamAI

# Page setup
st.set_page_config(page_title="Multilingual Chat", layout="wide")

# Load env
load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# Languages
LANGUAGES = {
    "English": "en-IN",
    "Bengali": "bn-IN",
    "Gujarati": "gu-IN",
    "Hindi": "hi-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Odia": "od-IN",
    "Punjabi": "pa-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN"
}

# Session init
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Function to handle sending messages
def send_message():
    user_input = st.session_state.user_input
    lang = st.session_state.lang

    if user_input.strip():
        st.session_state.messages.append(("user", user_input))

        # Call Sarvam AI API
        headers = {
            "Authorization": f"Bearer {SARVAM_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "sarvam-m",
            "messages": [{"role": "user", "content": user_input}]
        }
        response = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]

            # Translate if selected language is not English
            if LANGUAGES[lang] != "en-IN":
                reply = client.text.translate(
                    input=reply,
                    source_language_code="en-IN",
                    target_language_code=LANGUAGES[lang]
                ).translated_text

            st.session_state.messages.append(("assistant", reply))
        else:
            st.error(f"API Error: {response.status_code}")

        # Clear input after sending
        st.session_state.user_input = ""


# Display Logo (top-left)
st.markdown(
    """
    <div class="logo-container">
        <img src="https://cdn-icons-png.flaticon.com/128/9732/9732782.png" >
    </div>
    """,
    unsafe_allow_html=True
)

# Custom CSS
st.markdown(
    """
    <style>
    /* Logo top-left */
    .logo-container {
        position: absolute;
        top: 10px;
        left: 10px;
    }
    .logo-container img {
        width: 50px;
        height: auto;
    }

    /* Gradient background */
    .stApp {
        background: linear-gradient(to right, #6dd5fa, #2980b9);
        font-family: 'Helvetica', sans-serif;
    }

    /* Input/Output styling */
    .input-block, .output-block {
        background: transparent !important;
        box-shadow: none !important;
        padding: 20px;
    }

    .output-block {
        max-height: 70vh;
        overflow-y: auto;
    }

    /* Chat bubbles */
    .chat-message {
        display: flex;
        margin: 8px 0;
    }
    .chat-message.user {
        justify-content: flex-end;
    }
    .chat-message.assistant {
        justify-content: flex-start;
    }
    .user-msg {
        background: #1E90FF;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        max-width: 70%;
        word-wrap: break-word;
    }
    .assistant-msg {
        background: #10b981;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        max-width: 70%;
        word-wrap: break-word;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Layout: two columns
col1, col2 = st.columns([1, 2])

# Left Panel (Language Selection)
with col1:
    st.markdown('<div class="input-block">', unsafe_allow_html=True)
    st.header("😶‍🌫️ Select Language 👇")
    st.session_state.lang = st.selectbox("Language", list(LANGUAGES.keys()))
    st.markdown('</div>', unsafe_allow_html=True)

# Right Panel (Chat + Input)
with col2:
    st.markdown('<div class="output-block">', unsafe_allow_html=True)
    st.markdown(
        """
        <h2 style="text-align:center; margin: -2px 0 20px 0;">Chat Window 🐼</h2>
        """,
        unsafe_allow_html=True
    )

    # Display chat messages
    for role, msg in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div class='chat-message user'><div class='user-msg'>{msg}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message assistant'><div class='assistant-msg'>{msg}</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input & Send button with callback
    st.text_area("Enter your message", key="user_input")
    st.button("Send", on_click=send_message)



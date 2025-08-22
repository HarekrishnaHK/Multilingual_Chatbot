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

# Display the logo
st.markdown(
    """
    <div class="logo-container" style="position: absolute; top: 6px; left: 6px;">
        <img src="https://cdn-icons-png.flaticon.com/128/9732/9732782.png" >
    </div>
    """,
    unsafe_allow_html=True
)
# Custom CSS
st.markdown(
    """
    <style>
    /* Logo in top-left corner */
    .logo-container {
        position: absolute;
        top: 6px;
        left: 6px;
    }
    .logo-container img {
        width: 50px;  /* adjust size as needed */
        height: auto;
        display: inline-block;
    }

    /* Gradient background */
    .stApp {
        background: linear-gradient(to right, #6dd5fa, #2980b9);
        font-family: 'Helvetica', sans-serif;
    }

    /* Left input block */
    .input-block {
        background: transparent !important;
        box-shadow: none !important;
        padding: 20px;
    }

    /* Right chat block */
    .output-block {
        background: transparent !important;
        padding: 20px;
        max-height: 85vh;
        overflow-y: auto;
    }

    /* Chat message wrapper */
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

    /* Message bubbles */
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

with col1:
    st.markdown('<div class="input-block">', unsafe_allow_html=True)
    st.header("😶‍🌫️ Select Langeage 👇")
    lang = st.selectbox("Language", list(LANGUAGES.keys()))
    user_input = st.text_area("Enter your message")
    if st.button("Send"):
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
                # Translate if needed
                if LANGUAGES[lang] != "en-IN":
                    reply = client.text.translate(
                        input=reply,
                        source_language_code="en-IN",
                        target_language_code=LANGUAGES[lang]
                    ).translated_text
                st.session_state.messages.append(("assistant", reply))
            else:
                st.error(f"API Error: {response.status_code}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="output-block">', unsafe_allow_html=True)
    st.markdown(
        """
        <h2 style="text-align:center; margin: -2px 0 20px 0;">Chat Window 🐼</h2>
        """,
        unsafe_allow_html=True
    )
    for role, msg in st.session_state.messages:
        if role == "user":
            st.markdown(f"<div class='chat-message user'><div class='user-msg'>{msg}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-message assistant'><div class='assistant-msg'>{msg}</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

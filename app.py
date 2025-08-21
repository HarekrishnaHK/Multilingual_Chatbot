# import streamlit as st
# st.set_page_config(page_title="Multilingual Chat", layout="centered")  # must be first

# from sarvamai import SarvamAI
# from dotenv import load_dotenv
# import os
# import requests

# # Load environment variables
# load_dotenv()
# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# # Initialize SarvamAI client
# client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# # Define supported languages
# LANGUAGES = {
#     "English": "en-IN",
#     "Hindi": "hi-IN",
#     "Gujarati": "gu-IN",
#     "Bengali": "bn-IN",
#     "Kannada": "kn-IN",
#     "Punjabi": "pa-IN"
# }

# # Session state: active language
# if "active_lang" not in st.session_state:
#     st.session_state.active_lang = "English"

# # Session state: initialize chat & display history per language
# for lang in LANGUAGES:
#     if f"chat_history_{lang}" not in st.session_state:
#         st.session_state[f"chat_history_{lang}"] = [
#             {"role": "system", "content": "You are a helpful assistant."}
#         ]
#     if f"display_history_{lang}" not in st.session_state:
#         st.session_state[f"display_history_{lang}"] = []

# # Sidebar: language buttons
# st.sidebar.markdown("## 🌍 Select Language")
# for lang in LANGUAGES:
#     if st.sidebar.button(lang):
#         st.session_state.active_lang = lang

# # Get current language details
# current_lang = st.session_state.active_lang
# target_lang_code = LANGUAGES[current_lang]
# chat_history_key = f"chat_history_{current_lang}"
# display_history_key = f"display_history_{current_lang}"

# # App Title
# st.markdown(f"<h2 style='text-align: center;'>Multilingual Chat - {current_lang}</h2>", unsafe_allow_html=True)
# st.divider()

# # Display chat messages
# for chat in st.session_state[display_history_key]:
#     st.markdown(chat, unsafe_allow_html=True)

# # Chat input like GPT
# with st.form("chat_form", clear_on_submit=True):
#     user_input = st.text_input("You", placeholder="Type your message here...", label_visibility="collapsed")
#     submitted = st.form_submit_button("Send")

# if submitted and user_input.strip():
#     # Store user message
#     st.session_state[chat_history_key].append({"role": "user", "content": user_input})
#     st.session_state[display_history_key].append(
#         f"<div style='text-align: right; color: #1e90ff;'><strong>You:</strong> {user_input}</div>"
#     )
#     # Call Sarvam LLM
#     headers = {
#         "Authorization": f"Bearer {SARVAM_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model": "sarvam-m",
#         "messages": st.session_state[chat_history_key]
#     }

#     response = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload)

#     if response.status_code == 200:
#         assistant_reply = response.json()["choices"][0]["message"]["content"]

#         # Translate only if not already in target language
#         if target_lang_code != "en-IN":
#             translation = client.text.translate(
#                 input=assistant_reply,
#                 source_language_code="en-IN",
#                 target_language_code=target_lang_code,
#                 speaker_gender="Male"
#             )
#             final_reply = translation.translated_text
#         else:
#             final_reply = assistant_reply

#         # Store assistant response
#         st.session_state[chat_history_key].append({"role": "assistant", "content": final_reply})
#         st.session_state[display_history_key].append(
#             f"<div style='text-align: left; color: #10b981;'><strong>Assistant:</strong> {final_reply}</div>"
#         )
#     else:
#         st.error(f"API Error: {response.status_code} - {response.text}")







# import streamlit as st
# from dotenv import load_dotenv
# import os
# import requests
# from sarvamai import SarvamAI

# st.set_page_config(page_title="Multilingual Chat", layout="wide")

# # Load env
# load_dotenv()
# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
# client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# LANGUAGES = {
#     "English": "en-IN",
#     "Hindi": "hi-IN",
#     "Gujarati": "gu-IN",
#     "Bengali": "bn-IN",
#     "Kannada": "kn-IN",
#     "Punjabi": "pa-IN"
# }

# # Session init
# if "active_lang" not in st.session_state:
#     st.session_state.active_lang = "English"
# if "chats" not in st.session_state:
#     st.session_state.chats = {lang: [] for lang in LANGUAGES}

# # Sidebar
# st.sidebar.title("🌍 Language")
# st.session_state.active_lang = st.sidebar.radio("Choose:", list(LANGUAGES.keys()))

# current_lang = st.session_state.active_lang
# target_lang = LANGUAGES[current_lang]

# st.title(f"💬 Multilingual Chatbot ({current_lang})")

# chat_area = st.container()

# # Show chat as bubbles
# with chat_area:
#     for role, msg in st.session_state.chats[current_lang]:
#         if role == "user":
#             st.markdown(f"<div style='text-align:right;background:#DCF8C6;padding:10px;border-radius:10px;margin:5px'>{msg}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='text-align:left;background:#E5E5EA;padding:10px;border-radius:10px;margin:5px'>{msg}</div>", unsafe_allow_html=True)

# # Input
# user_input = st.chat_input("Type your message...")

# if user_input:
#     st.session_state.chats[current_lang].append(("user", user_input))

#     # Call Sarvam API
#     headers = {"Authorization": f"Bearer {SARVAM_API_KEY}", "Content-Type": "application/json"}
#     payload = {"model": "sarvam-m", "messages": [{"role": "user", "content": user_input}]}
#     response = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload)

#     if response.status_code == 200:
#         reply = response.json()["choices"][0]["message"]["content"]

#         if target_lang != "en-IN":
#             reply = client.text.translate(input=reply, source_language_code="en-IN", target_language_code=target_lang).translated_text

#         st.session_state.chats[current_lang].append(("assistant", reply))
#     else:
#         st.error("API error")




# import streamlit as st
# from dotenv import load_dotenv
# import os
# import requests
# from sarvamai import SarvamAI

# st.set_page_config(page_title="Multilingual Chat", layout="centered")

# load_dotenv()
# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
# client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# LANGUAGES = {
#     "English": "en-IN",
#     "Hindi": "hi-IN",
#     "Gujarati": "gu-IN",
#     "Bengali": "bn-IN",
#     "Kannada": "kn-IN",
#     "Punjabi": "pa-IN"
# }

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = {lang: [] for lang in LANGUAGES}

# st.title("🗣️ Multilingual Chatbot")

# tabs = st.tabs(list(LANGUAGES.keys()))

# for i, lang in enumerate(LANGUAGES.keys()):
#     with tabs[i]:
#         st.subheader(f"{lang} Chat")
#         for role, msg in st.session_state.chat_history[lang]:
#             st.write(f"**{role.title()}**: {msg}")

#         user_input = st.text_input(f"Message in {lang}", key=f"input_{lang}")
#         if st.button(f"Send ({lang})", key=f"btn_{lang}"):
#             st.session_state.chat_history[lang].append(("user", user_input))
#             headers = {"Authorization": f"Bearer {SARVAM_API_KEY}", "Content-Type": "application/json"}
#             payload = {"model": "sarvam-m", "messages": [{"role": "user", "content": user_input}]}
#             response = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload)

#             if response.status_code == 200:
#                 reply = response.json()["choices"][0]["message"]["content"]
#                 if LANGUAGES[lang] != "en-IN":
#                     reply = client.text.translate(input=reply, source_language_code="en-IN", target_language_code=LANGUAGES[lang]).translated_text
#                 st.session_state.chat_history[lang].append(("assistant", reply))



# it is correct


# import streamlit as st
# from dotenv import load_dotenv
# import os
# import requests
# from sarvamai import SarvamAI

# st.set_page_config(page_title="Multilingual Chat", layout="wide")

# load_dotenv()
# SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
# client = SarvamAI(api_subscription_key=SARVAM_API_KEY)

# LANGUAGES = {
#     "Bengali": "bn-IN",
#     "English": "en-IN",
#     "Gujarati": "gu-IN",
#     "Hindi": "hi-IN",
#     "Kannada": "kn-IN",
#     "Malayalam": "ml-IN",
#     "Marathi": "mr-IN",
#     "Odia": "od-IN",
#     "Punjabi": "pa-IN",
#     "Tamil": "ta-IN",
#     "Telugu": "te-IN"
# }

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# col1, col2 = st.columns([1,2])

# with col1:
#     st.header("⚙️ Settings")
#     lang = st.selectbox("Language", list(LANGUAGES.keys()))

#     user_input = st.text_area("Enter your message")
#     if st.button("Send"):
#         st.session_state.messages.append(("user", user_input))

#         headers = {"Authorization": f"Bearer {SARVAM_API_KEY}", "Content-Type": "application/json"}
#         payload = {"model": "sarvam-m", "messages": [{"role": "user", "content": user_input}]}
#         response = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload)

#         if response.status_code == 200:
#             reply = response.json()["choices"][0]["message"]["content"]
#             if LANGUAGES[lang] != "en-IN":
#                 reply = client.text.translate(input=reply, source_language_code="en-IN", target_language_code=LANGUAGES[lang]).translated_text
#             st.session_state.messages.append(("assistant", reply))

# with col2:
#     st.header("💬 Chat Window")
#     for role, msg in st.session_state.messages:
#         if role == "user":
#             st.markdown(f"<div style='text-align:right;color:#1E90FF'><b>You:</b> {msg}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div style='text-align:left;color:#10b981'><b>Assistant:</b> {msg}</div>", unsafe_allow_html=True)


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

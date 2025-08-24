import os
import datetime
import requests
import streamlit as st
import wikipedia
from dotenv import load_dotenv

# Place config FIRST
st.set_page_config(page_title="Multilingual Chatbot", layout="wide", page_icon="🤖")

# ---- LLMs ----
import google.generativeai as genai          # Gemini
from sarvamai import SarvamAI                # Sarvam (chat + translate)

# =============================
#  ENV & CLIENTS
# =============================
load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY) if SARVAM_API_KEY else None

gemini_model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# =============================
#  APP CONFIG
# =============================
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
    "Telugu": "te-IN",
}

# =============================
#  STYLES
# =============================
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

      :root{
        --app-bg: #f3f4f6;
        --text-main: #111827;
        --text-muted: #4b5563;
        --border: #e5e7eb;

        --left-bg: #e6f0ff;
        --left-text: #0f172a;
        --left-border: #c7d7ff;

        --chat-card: #ffffff;
        --chat-header-bg: #1f2a44;
        --chat-header-text: #ffffff;
        --messages-bg: #fafafa;

        --bubble-user-bg: #2563eb;
        --bubble-user-text: #ffffff;
        --bubble-bot-bg: #ffffff;
        --bubble-bot-border: #e5e7eb;

        --input-bg: #ffffff;
        --input-border: #d1d5db;
        --input-focus: #2563eb;
        --btn-bg: #2563eb;
        --btn-text: #ffffff;
        --btn-danger-bg: #dc2626;
        --btn-danger-text: #ffffff;
      }

      .stApp{
        background: var(--app-bg);
        color: var(--text-main);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
      }

      .block-container{
        padding: 16px 16px 0 16px !important;
        max-width: 100% !important;
      }

      .main-container{ max-width: 1400px; margin: 0 auto; padding: 8px; }

      section[data-testid="stSidebar"]{
        background: var(--left-bg) !important;
        border-right: 1px solid var(--left-border) !important;
      }

      .settings-title{
        font-size: 18px; font-weight: 700; margin-bottom: 8px; color: var(--left-text);
      }
      .setting-label{
        font-size: 13px; font-weight: 600; color: var(--text-muted);
        margin: 8px 0 4px 0;
      }

      .chat-container{
        background: var(--chat-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        height: 85vh;
        display: flex;
        flex-direction: column;
      }
      .chat-header{
        background: var(--chat-header-bg);
        color: var(--chat-header-text);
        padding: 14px 18px;
        text-align: center;
      }
      .chat-title{ font-size: 20px; font-weight: 700; margin: 0; }
      .chat-subtitle{ font-size: 12px; opacity: 0.9; margin-top: 2px; }

      .chat-messages{
        background: var(--messages-bg);
        flex: 1;
        padding: 14px 16px;
        overflow-y: auto;
      }
      .message-bubble{
        max-width: 75%;
        padding: 10px 14px;
        margin: 8px 0;
        border-radius: 12px;
        font-size: 14px;
        line-height: 1.45;
        word-wrap: break-word;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
      }
      .message-user{
        margin-left: auto;
        background: var(--bubble-user-bg);
        color: var(--bubble-user-text);
        border-bottom-right-radius: 4px;
      }
      .message-bot{
        margin-right: auto;
        background: var(--bubble-bot-bg);
        color: var(--text-main);
        border: 1px solid var(--bubble-bot-border);
        border-bottom-left-radius: 4px;
      }

      .chat-input-area{
        background: #f7f7f7;
        border-top: 1px solid var(--border);
        padding: 12px;
      }

      .stSelectbox > div > div{
        background: var(--input-bg);
        border: 1px solid var(--input-border);
        border-radius: 10px;
        height: 42px;
        font-size: 13px;
      }
      .stTextInput > div > div > input{
        background: var(--input-bg) !important;
        border: 1px solid var(--input-border) !important;
        border-radius: 10px !important;
        height: 42px !important;
        padding: 0 12px !important;
        font-size: 14px !important;
      }
      .stTextInput > div > div > input:focus{
        border-color: var(--input-focus) !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important;
        outline: none !important;
      }

      .stButton > button{
        background: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
      }

      .clear-button button{
        background: var(--btn-danger-bg) !important;
        color: var(--btn-danger-text) !important;
      }

      @media (max-width: 768px){
        .chat-container{ height: 80vh; }
        .message-bubble{ max-width: 90%; }
      }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
#  STATE
# =============================
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []
if "llm_messages_en" not in st.session_state:
    st.session_state.llm_messages_en = [{"role": "system", "content": "You are a helpful assistant."}]

# =============================
#  HELPERS
# =============================
def translate_text(text: str, src_code: str, tgt_code: str) -> str:
    if not text or src_code == tgt_code:
        return text
    if not sarvam_client:
        return text
    try:
        tr = sarvam_client.text.translate(
            input=text,
            source_language_code=src_code,
            target_language_code=tgt_code,
        )
        return tr.translated_text
    except Exception:
        return text

def sarvam_chat_completion(messages_en):
    if not SARVAM_API_KEY:
        return "⚠️ SARVAM_API_KEY missing."
    try:
        headers = {"Authorization": f"Bearer {SARVAM_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "sarvam-m", "messages": messages_en}
        r = requests.post("https://api.sarvam.ai/v1/chat/completions", headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        return f"⚠️ Sarvam API error {r.status_code}: {r.text}"
    except Exception as e:
        return f"⚠️ Sarvam request failed: {e}"

def gemini_generate(prompt: str) -> str:
    if not gemini_model:
        return "⚠️ GEMINI_API_KEY missing."
    try:
        resp = gemini_model.generate_content(prompt)
        return getattr(resp, "text", "").strip() or "⚠️ Empty response from Gemini."
    except Exception as e:
        return f"⚠️ Gemini error: {e}"

def wiki_search(query):
    try:
        return wikipedia.summary(query, sentences=2, auto_suggest=True)
    except Exception:
        return "⚠️ Wikipedia lookup failed."

def local_tools(query_en: str):
    q = query_en.lower()
    if "date" in q:
        return f"📅 Today's date is {datetime.date.today().strftime('%B %d, %Y')}."
    if "time" in q:
        return f"⏰ The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    if "wikipedia" in q or q.startswith("who is") or q.startswith("what is"):
        topic = (
            query_en.replace("wikipedia", "", 1)
                    .replace("Who is", "", 1).replace("who is", "", 1)
                    .replace("What is", "", 1).replace("what is", "", 1)
        ).strip()
        if not topic:
            return "📖 Please specify a topic for Wikipedia."
        return "📖 " + wiki_search(topic)
    return None

# =============================
#  LAYOUT
# =============================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Sidebar: Language Settings
with st.sidebar:
    st.markdown('### 🌐 Language Settings')
    input_lang_name = st.selectbox("Input Language", list(LANGUAGES.keys()), index=0, key="sel_input_lang")
    output_lang_name = st.selectbox("Output Language", list(LANGUAGES.keys()), index=0, key="sel_output_lang")
    st.caption(
        f"Selected: input={input_lang_name} ({LANGUAGES[input_lang_name]}), "
        f"output={output_lang_name} ({LANGUAGES[output_lang_name]})"
    )
    st.markdown('<div class="clear-button">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_btn"):
        st.session_state.chat_display = []
        st.session_state.llm_messages_en = [{"role": "system", "content": "You are a helpful assistant."}]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Main content columns: make sure to UNPACK correctly and only use `with` on containers
main_col ,= st.columns([1])
with main_col:
    st.markdown(
        '<div class="chat-header">'
        '<div class="chat-title">🤖 Multilingual AI Assistant</div>'
        '<div class="chat-subtitle">Powered by SarvamAI & Gemini</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Messages
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    if not st.session_state.chat_display:
        st.markdown(
            '<div style="text-align: center; padding: 60px 20px; color: #718096;">'
            '<div style="font-size: 48px; margin-bottom: 16px;">💬</div>'
            '<div style="font-size: 18px; font-weight: 500;">Start a conversation</div>'
            '<div style="font-size: 14px; margin-top: 8px;">Type your message below to begin chatting</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        for m in st.session_state.chat_display:
            cls = "message-user" if m["role"] == "user" else "message-bot"
            st.markdown(f'<div class="message-bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Input Area
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)

    # Create two columns correctly and UNPACK them
    col_model, col_input = st.columns([1.5, 6])

    with col_model:
        model_choice = st.selectbox(
            "AI Model",
            ["SarvamAI", "Gemini"],
            index=0,
            key="sel_model_choice",
            help="Choose which backend to use for replies"
        )

    with col_input:
        with st.form("send_form", clear_on_submit=True):
            user_text = st.text_input(
                "Message",
                value="",
                placeholder=f"Type your message in {input_lang_name} and press Enter...",
            )
            submitted = st.form_submit_button("Send", use_container_width=True)
            if submitted and user_text.strip():
                st.session_state._pending_user_text = user_text

    # Handle message sending
    user_text_from_enter = st.session_state.pop("_pending_user_text", None) if "_pending_user_text" in st.session_state else None
    final_user_text = user_text_from_enter

    if final_user_text and final_user_text.strip():
        st.session_state.chat_display.append({"role": "user", "content": final_user_text})

        src_code = LANGUAGES[input_lang_name]
        msg_en = translate_text(final_user_text, src_code, "en-IN")

        reply_en = local_tools(msg_en)
        if not reply_en:
            if model_choice == "SarvamAI":
                st.session_state.llm_messages_en.append({"role": "user", "content": msg_en})
                reply_en = sarvam_chat_completion(st.session_state.llm_messages_en)
                st.session_state.llm_messages_en.append({"role": "assistant", "content": reply_en})
            else:
                steer = "Reply in English. I will translate your answer for the user." if sarvam_client else f"Reply in {output_lang_name}."
                prompt = f"{steer}\n\nUser: {msg_en}"
                reply_en = gemini_generate(prompt)

        tgt_code = LANGUAGES[output_lang_name]
        final_reply = translate_text(reply_en, "en-IN", tgt_code) if sarvam_client else reply_en

        st.session_state.chat_display.append({"role": "assistant", "content": final_reply})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # chat-container

st.markdown('</div>', unsafe_allow_html=True)  # main-container

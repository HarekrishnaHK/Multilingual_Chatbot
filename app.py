import os
import datetime
import requests
import streamlit as st
from dotenv import load_dotenv

# Optional convenience (used for simple wiki fallback if desired later)
# import wikipedia

# LLM SDKs
import google.generativeai as genai  # Gemini
from sarvamai import SarvamAI        # Sarvam (translate helper)

# ---------- Page setup ----------
st.set_page_config(page_title="Multilingual Chat UI", layout="wide", page_icon="🤖")

# ---------- Env & clients ----------
load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY) if SARVAM_API_KEY else None

gemini_model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- Languages ----------
# Keys: display names; Values: Sarvam language codes for translation
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

# ---------- Styles ----------
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
    unsafe_allow_html=True,
)

# ---------- State ----------
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []  # [{'role': 'user'|'assistant', 'content': str}]
if "llm_messages_en" not in st.session_state:
    st.session_state.llm_messages_en = [{"role": "system", "content": "You are a helpful assistant."}]

# ---------- Helpers ----------
def translate_text(text: str, src_code: str, tgt_code: str) -> str:
    """Translate using Sarvam if available; otherwise passthrough."""
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
    """Sarvam OpenAI-compatible chat completions."""
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
    """Generate via Gemini; simple text call."""
    if not gemini_model:
        return "⚠️ GEMINI_API_KEY missing."
    try:
        resp = gemini_model.generate_content(prompt)
        return getattr(resp, "text", "").strip() or "⚠️ Empty response from Gemini."
    except Exception as e:
        return f"⚠️ Gemini error: {e}"

def local_tools(query_en: str):
    """Small utilities: return current local date/time if asked."""
    if not query_en:
        return None
    q = query_en.lower()
    if "time" in q:
        # Local server time; customize timezone if needed
        return f"⏰ The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    if "date" in q or "today" in q:
        return f"📅 Today's date is {datetime.date.today().strftime('%B %d, %Y')}."
    return None

# ---------- Sidebar controls ----------
with st.sidebar:
    st.markdown('### 🌐 Language Settings 👇')
    input_lang_name = st.selectbox("Input Language", list(LANGUAGES.keys()), index=0, key="sel_input_lang")
    output_lang_name = st.selectbox("Output Language", list(LANGUAGES.keys()), index=0, key="sel_output_lang")
    st.caption(
        f"Selected: input={input_lang_name} ({LANGUAGES[input_lang_name]}), "
        f"output={output_lang_name} ({LANGUAGES[output_lang_name]})"
    )
    st.markdown('### ⚙️ Model')
    model_choice = st.selectbox(
        "👉 Choose any model",
        ["Syntera", "Gravion"],
        index=0,
        key="sel_model_choice",
        help="Choose which model you use for replies",
    )
    st.markdown('<div class="clear-button">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_btn"):
        st.session_state.chat_display = []
        st.session_state.llm_messages_en = [{"role": "system", "content": "You are a helpful assistant."}]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Main layout ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Chat container + header (Powered by SarvamAI & Gemini)
st.markdown(
    # '<div class="chat-container">'
    '<div class="chat-header">'
    '<div class="chat-title"> Multilingual AI Assistant 🐼</div>'
    '<div class="chat-subtitle"></div>'
    '</div>',
    unsafe_allow_html=True,
)

# Messages area
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
if not st.session_state.chat_display:
    st.markdown(
        '<div style="text-align: center; padding: 60px 20px; color: #718096;">'
        '<div style="font-size: 48px; margin-bottom: 16px;">💬</div>'
        '<div style="font-size: 18px; font-weight: 500;">Start a conversation</div>'
        '<div style="font-size: 14px; margin-top: 8px;">Type your message below to begin chat with me 👍</div>'
        '</div>',
        unsafe_allow_html=True
    )
else:
    for m in st.session_state.chat_display:
        cls = "message-user" if m["role"] == "user" else "message-bot"
        st.markdown(f'<div class="message-bubble {cls}">{m["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input area with model selector
st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
col_input, = st.columns([1])

with col_input:
    with st.form("send_form", clear_on_submit=True):
        user_text = st.text_input(
            "Message",
            value="",
            placeholder=f"Type your message in {input_lang_name} and press Enter...",
        )
        submitted = st.form_submit_button("Send", use_container_width=True)
        if submitted and user_text.strip():
            # Record user message as-is for display
            st.session_state.chat_display.append({"role": "user", "content": user_text})

            # Normalize to English for model
            src_code = LANGUAGES[input_lang_name]
            msg_en = (
                user_text if src_code == "en-IN"
                else translate_text(user_text, src_code, "en-IN")
            )

            # Local quick tools: time/date
            reply_en = local_tools(msg_en)

            # If not handled locally, call chosen model
            if not reply_en:
                if model_choice == "SarvamAI":
                    # Maintain minimal conversation context for Sarvam
                    st.session_state.llm_messages_en.append({"role": "user", "content": msg_en})
                    reply_en = sarvam_chat_completion(st.session_state.llm_messages_en)
                    st.session_state.llm_messages_en.append({"role": "assistant", "content": reply_en})
                else:
                    # Gemini: request English for consistent translation downstream
                    steer = "Reply in English. I will translate your answer for the user." if sarvam_client else f"Reply in {output_lang_name}."
                    prompt = f"{steer}\n\nUser: {msg_en}"
                    reply_en = gemini_generate(prompt)

            # Translate to target output language if needed
            tgt_code = LANGUAGES[output_lang_name]
            final_reply = (
                reply_en if tgt_code == "en-IN"
                else translate_text(reply_en, "en-IN", tgt_code)
            )

            # Display assistant reply
            st.session_state.chat_display.append({"role": "assistant", "content": final_reply})
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)   # chat-input-area
st.markdown('</div>', unsafe_allow_html=True)   # chat-container
st.markdown('</div>', unsafe_allow_html=True)   # main-container

Here’s a polished **README.md** for your chatbot project 👇

```markdown
# 🌍 Multilingual Chatbot (SarvamAI + Gemini + Streamlit)

A modern multilingual chatbot built with **SarvamAI API**, **Google Gemini**, and **Streamlit**, supporting multiple Indian languages with real-time translation.  

👉 [**Live Demo**](https://multilanguage-hk-bot.onrender.com)

---

## 📂 Project Structure

```

Multilingual\_chat/
│── app.py              # Main Streamlit app
│── requirements.txt    # Dependencies
│── .env                # API keys
│── README.md           # Documentation
│── assets/
└── preview\.png     # App screenshot

````

---

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone <your_repo_url>
   cd Multilingual_chat
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** → create a `.env` file:

   ```ini
   SARVAM_API_KEY=your_sarvam_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

   Open in your browser 👉 [http://localhost:8501](http://localhost:8501)

---

## 🌐 Supported Languages

* English (en-IN)
* Bengali (bn-IN)
* Gujarati (gu-IN)
* Hindi (hi-IN)
* Kannada (kn-IN)
* Malayalam (ml-IN)
* Marathi (mr-IN)
* Odia (od-IN)
* Punjabi (pa-IN)
* Tamil (ta-IN)
* Telugu (te-IN)

---

## ✨ Features

* 🔄 **Translate seamlessly** between input/output languages
* 🤖 **Choose AI backend**: SarvamAI or Gemini
* 📖 **Built-in tools**: Date, time, and Wikipedia summaries
* 🧹 **Clear chat history** with one click
* 📱 **Responsive design** with custom styling

---

## 🖼️ Preview

[![App Screenshot](assets/preview.png)](https://multilanguage-hk-bot.onrender.com)

---

🚀 Start chatting in your own language today!

```
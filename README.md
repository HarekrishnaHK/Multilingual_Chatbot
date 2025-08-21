```markdown
# 🌍 Multilingual Chatbot using Sarvam AI + Streamlit

A multilingual chatbot built with **Sarvam AI API** and **Streamlit**, supporting multiple Indian languages.

---

## 📂 Project Structure

```

Multilingual\_chat/
│── .env
│── requirements.txt
│── app.py
│── README.md

````

---

## ⚙️ Setup Instructions

1. **Clone repo or create folder**
   ```bash
   mkdir Multilingual_chat && cd Multilingual_chat
````

2. **Create virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Linux/Mac
   venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set API Key**

   * Create a `.env` file in the root directory.
   * Add:

     ```ini
     SARVAM_API_KEY=your_api_key_here
     ```

5. **Run the chatbot**

   ```bash
   streamlit run app.py
   ```

6. **Open in browser**

   * Navigate to `http://localhost:8501`

---

## 🌐 Supported Languages

* English
* Hindi
* Gujarati
* Bengali
* Kannada
* Punjabi

---

## 📝 Notes

* Default language is **English**.
* Assistant reply is **translated** into selected language if not English.
* Uses **SarvamAI LLM + Translation API**.

---

🚀 Now you can chat in multiple languages!

```



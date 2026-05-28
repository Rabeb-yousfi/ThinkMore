import streamlit as st
import google.generativeai as genai
import json

# إعدادات الصفحة
st.set_page_config(page_title="فكر أكثر | thinkMore - ذكاء اصطناعي", page_icon="🧠", layout="centered")

# الحقن الشامل للـ RTL
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp, html, body {
        direction: RTL !important;
        text-align: right !important;
    }
    .centered-content {
        text-align: center !important;
        direction: RTL !important;
        display: block;
        width: 100%;
    }
    div.stButton > button {
        width: 100%;
        direction: RTL !important;
    }
    </style>
""", unsafe_allow_html=True)

# 🔑 السطر الذي يبحث عن المفتاح في إعدادات السيرفر (Secrets)
API_KEY = st.secrets["GEMINI_KEY = "AIzaSyRB708...""]

# دالة توليد الأفكار
def generate_nebula_idea(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """
        أنت باحث متخصص في تفكيك "نهج البلاغة". اختر حكمة عشوائية وقم بصياغة المخرجات بصيغة JSON حصراً:
        {
          "category": "تصنيف الفكرة",
          "title": "عنوان جذاب",
          "content": "النص الشريف",
          "deep_dive_markdown": "### ورقة بحثية... (محتوى الماركداون)"
        }
        """
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        return None

# --- واجهة التطبيق ---
st.markdown("<div class='centered-content'><h1>🧠 فكر أكثر | thinkMore AI</h1></div>", unsafe_allow_html=True)

if 'ai_idea' not in st.session_state:
    st.session_state.ai_idea = generate_nebula_idea(API_KEY)

idea = st.session_state.ai_idea

if idea:
    with st.container(border=True):
        st.markdown(f"### 📜 {idea.get('title')}")
        st.markdown(f"<p>{idea.get('content')}</p>", unsafe_allow_html=True)

    if st.button("🔄 توليد حكمة جديدة"):
        st.session_state.ai_idea = generate_nebula_idea(API_KEY)
        st.rerun()
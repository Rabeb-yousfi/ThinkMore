import streamlit as st
import google.generativeai as genai
import json
import os

# إعداد الصفحة وتوسيط العناوين وتنسيق RTL
st.set_page_config(page_title="فكر أكثر | thinkMore", layout="centered")

st.markdown("""
    <style>
        .stApp { direction: rtl; text-align: right; }
        h1, h2, h3 { text-align: center; }
        .wisdom-text { font-size: 1.2em; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# استرجاع المفتاح بشكل آمن
api_key = st.secrets.get("GEMINI_KEY")

if not api_key:
    st.error("خطأ: مفتاح GEMINI_KEY غير موجود في الإعدادات. يرجى مراجعة تبويب Secrets.")
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"خطأ في تهيئة النموذج: {e}")

st.title("💡 فكر أكثر | thinkMore")
st.subheader("استخراج وتحليل حكم نهج البلاغة")

if 'wisdom_data' not in st.session_state:
    st.session_state.wisdom_data = None

def get_new_wisdom():
    prompt = """
    أعطني حكمة واحدة من نهج البلاغة.
    أريدك أن ترجع النتيجة بصيغة JSON فقط، تحتوي على المفاتيح التالية:
    {"category": "التصنيف", "title": "العنوان", "text": "النص", "analysis": "التحليل الاستراتيجي"}
    """
    try:
        response = model.generate_content(prompt)
        # محاولة تنظيف النص
        content = response.text.strip().replace("```json", "").replace("```", "")
        st.session_state.wisdom_data = json.loads(content)
    except Exception as e:
        st.error(f"فشل الاتصال بـ API: {str(e)}")

# زر التوليد
if st.button("توليد حكمة جديدة"):
    with st.spinner('جاري التفكير...'):
        get_new_wisdom()

# عرض النتائج
if st.session_state.wisdom_data:
    data = st.session_state.wisdom_data
    st.markdown(f"## {data['title']}")
    st.markdown(f"**التصنيف:** {data['category']}")
    st.markdown(f"<div class='wisdom-text'>{data['text']}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔍 التحليل الاستراتيجي")
    st.write(data['analysis'])

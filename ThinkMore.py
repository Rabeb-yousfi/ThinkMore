import streamlit as st
import google.generativeai as genai
import json

# إعداد الواجهة لتكون RTL
st.set_page_config(page_title="فكر أكثر | thinkMore", layout="centered")
st.markdown("""
    <style>
        .stApp { direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

# إعداد الـ API
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("خطأ في إعداد الاتصال بمزود الخدمة. تأكد من إعداد المفتاح في الـ Secrets.")

st.title("💡 فكر أكثر | thinkMore")
st.subheader("استخراج وتحليل حكم نهج البلاغة")

# التخزين المؤقت للحالة
if 'wisdom_data' not in st.session_state:
    st.session_state.wisdom_data = None

def get_new_wisdom():
    prompt = """
    أعطني حكمة واحدة من نهج البلاغة.
    أريدك أن ترجع النتيجة بصيغة JSON فقط، تحتوي على المفاتيح التالية:
    {"category": "التصنيف", "title": "العنوان", "text": "النص", "analysis": "التحليل الاستراتيجي للقيادة والحياة"}
    لا تضف أي نص خارج نطاق الـ JSON.
    """
    try:
        response = model.generate_content(prompt)
        # تنظيف النص من علامات markdown في حال وجودها
        raw_text = response.text.replace("```json", "").replace("```", "")
        st.session_state.wisdom_data = json.loads(raw_text)
    except Exception as e:
        st.error("حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. حاول مرة أخرى.")

if st.button("توليد حكمة جديدة"):
    get_new_wisdom()

if st.session_state.wisdom_data:
    data = st.session_state.wisdom_data
    st.success(f"### {data['title']}")
    st.info(f"**التصنيف:** {data['category']}")
    st.write(f"**النص:** {data['text']}")
    st.warning(f"### 🔍 التحليل الاستراتيجي\n{data['analysis']}")
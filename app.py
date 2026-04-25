import streamlit as st
import google.generativeai as genai
import os

# إعداد الصفحة
st.set_page_config(page_title="مختبر محلل البينة", layout="wide")

# 1. تحميل النص المرجعي (quran.txt)
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return "خطأ: ملف quran.txt غير موجود في المستودع."

full_text = load_data()

# 2. القائمة الجانبية لإدارة المحركات
st.sidebar.title("⚙️ غرفة التحكم")

# اختيار النسخة المطلوبة حصراً
gemini_version = st.sidebar.selectbox(
    "اختر النسخة للتجربة:", 
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
)

# الربط بالمفتاح من Secrets مباشرة
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # إعداد المحرك المختار
        model = genai.GenerativeModel(model_name=gemini_version)
    except Exception as e:
        st.sidebar.error(f"خطأ في إعداد الموديل: {e}")
else:
    st.sidebar.warning("⚠️ لم يتم العثور على API KEY في Advanced Settings.")

# 3. واجهة المختبر (بدون كلمة سر)
st.title(f"🔬 مختبر التحليل المادي ({gemini_version})")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال الطلبات
if prompt := st.chat_input("أدخل تساؤلك للمختبر..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if api_key and full_text:
        with st.chat_message("assistant"):
            try:
                # إرسال البيانات للمحرك
                context_prompt = f"النص المرجعي:\n{full_text}\n\nالمهمة: {prompt}"
                response = model.generate_content(context_prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"بينة الفشل التقني: {e}")

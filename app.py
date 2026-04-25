import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مختبر Gemini المتكامل", layout="wide")

# 1. نظام الحماية
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets.get("MY_PASSWORD", "123456"):
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. قراءة البينة (quran.txt)
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 3. واجهة التحكم (اختيار النسخة)
st.sidebar.title("⚙️ خيارات Gemini")

# هنا وضعت لك النسخ التي طلبتها بالضبط لتجربتها
gemini_version = st.sidebar.selectbox(
    "اختر نسخة الموديل للتجربة:", 
    ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
)

# خانة API يدوية (ضرورية جداً إذا وقع خطأ 404)
user_key = st.sidebar.text_input("أدخل API Key هنا:", type="password")
final_key = user_key if user_key else st.secrets.get("GOOGLE_API_KEY")

# 4. تفعيل المحرك المختار
model = None
if final_key:
    genai.configure(api_key=final_key)
    try:
        # الربط المباشر بالنسخة المختارة من القائمة
        model = genai.GenerativeModel(model_name=gemini_version)
        st.sidebar.success(f"تم اختيار: {gemini_version}")
    except Exception as e:
        st.sidebar.error(f"الموديل غير مدعوم: {e}")
else:
    st.sidebar.warning("⚠️ الصق الـ API Key في الخانة أعلاه.")

# 5. واجهة الشات
st.title(f"💬 تجربة محرك: {gemini_version}")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("اسأل الموديل المختار..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    if model and full_text:
        with st.chat_message("assistant"):
            try:
                # إرسال النص مع الطلب
                response = model.generate_content(f"النص المرجعي:\n{full_text}\n\nالطلب: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطأ في الاستجابة: {e}")

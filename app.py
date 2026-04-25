import streamlit as st
import google.generativeai as genai
import os

# إعدادات الواجهة
st.set_page_config(page_title="محلل البينة", layout="wide")

# 1. نظام الدخول
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets["MY_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. التأكد من الملف
if not os.path.exists("quran.txt"):
    st.error("❌ ملف quran.txt غير موجود في GitHub!")
    st.stop()

with open("quran.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# 3. إعداد الوكلاء والـ API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
agent_role = st.sidebar.selectbox("الوكيل:", ["وكيل الجمع 📚", "وكيل النقد ⚖️"])

# استخدام فلاش لتجنب خطأ NotFound
model = genai.GenerativeModel('gemini-1.5-flash') 

st.title(f"💬 {agent_role}")
st.success("✅ البينة جاهزة.")

# 4. الشات
if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("ادخل تساؤلك..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = model.generate_content(f"النص المرجعي:\n{full_text}\n\nالمهمة: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ في الـ API: {e}")

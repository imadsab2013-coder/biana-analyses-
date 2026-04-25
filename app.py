import streamlit as st
import google.generativeai as genai
import os

# --- الهيكل المفتوح المصدر المعدل ---
st.title("🔬 مختبر البينة (Gemini Edition)")

# جلب المفتاح من Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ لم نجد المفتاح في Secrets!")
    st.stop()

# إعداد الموديل (نختار Flash لأنه الأكثر استقراراً في القوالب الجاهزة)
model = genai.GenerativeModel('gemini-1.5-flash')

# تحميل ملف quran.txt
if os.path.exists("quran.txt"):
    with open("quran.txt", "r", encoding="utf-8") as f:
        quran_context = f.read()
else:
    quran_context = ""

# نظام الشات القياسي (Open Source Template)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("أدخل تساؤلك التحليلي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # دمج السياق مع السؤال
            full_prompt = f"استناداً للنص التالي:\n{quran_context}\n\nالسؤال: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"فشل الاتصال بالمحرك: {e}")

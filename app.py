import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="محلل البينة - المختبر المتكامل", layout="wide")

# 1. نظام الحماية
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets.get("MY_PASSWORD", "123456"):
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. تحميل ملف القرآن (quran.txt)
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 3. إعدادات القائمة الجانبية (الاختيار بين المحركات والوكلاء)
st.sidebar.title("⚙️ غرفة التحكم")

# اختيار المحرك (AI Model)
ai_provider = st.sidebar.selectbox("اختر المحرك (AI Provider):", ["Google Gemini",

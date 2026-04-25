import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مختبر البينة", layout="wide")

# 1. تحميل النص المرجعي
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 2. الإعدادات الجانبية
st.sidebar.title("⚙️ الإعدادات المادية")

models_dict = {
    "Gemini 1.5 Flash": "models/gemini-1.5-flash",
    "Gemini 1.5 Pro": "models/gemini-1.5-pro",
    "Gemini 2.0 Flash": "models/gemini-2.0-flash-exp"
}

version_label = st.sidebar.selectbox("اختر النسخة:", list(models_dict.keys()))
model_path = models_dict[version_label]

api_key = st.secrets.get("GOOGLE_API_KEY")

# --- نظام البولة (Indicator) ---
connection_status = False
if api_key:
    try:
        genai.configure(api_key=api_key)
        # تصحيح السطر الذي سبب الخطأ
        model = genai.GenerativeModel(model_name=model_path)
        connection_status = True
        st.sidebar.success(f"🟢 متصل: {version_label}")
    except Exception as e:
        st.sidebar.error(f"🔴 خطأ: {version_label}")
        connection_status = False
else:
    st.sidebar.warning("⚪ في انتظار المفتاح")

# 3. الواجهة الرئيسية
st.title(f"🔬 تحليل: {version_label}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("اسأل المختبر..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if connection_status and full_text:
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(f"سياق:\n{full_text}\n\nطلب:\n{prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"⚠️ فشل: {e}")

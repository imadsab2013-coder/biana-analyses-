import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مختبر محلل البينة", layout="wide")

# 1. الحماية
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets["MY_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. قراءة الملف
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 3. إعدادات الوكلاء
agents = {
    "وكيل الجمع 📚": "أنت وكيل الجمع. استخرج الآيات المرتبطة بالطلب من النص المرفق فقط بدون زيادة أو تفسير.",
    "وكيل النقد الصارم ⚖️": "أنت المحقق الصارم. ابحث عن الثغرات والاتساق المنطقي في النصوص المجموعة."
}

st.sidebar.title("🤖 التحكم")
agent_choice = st.sidebar.selectbox("الوكيل:", list(agents.keys()))

# ربط الـ API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=agents[agent_choice])

# 4. الشات
st.title(f"💬 {agent_choice}")
if not full_text: st.error("⚠️ ملف quran.txt غير موجود.")
else: st.success("✅ البينة جاهزة.")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("اسأل الوكيل..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = model.generate_content(f"النص المرجعي:\n{full_text}\n\nالطلب: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

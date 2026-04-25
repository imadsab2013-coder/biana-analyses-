import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="محلل البينة", layout="wide")

# 1. نظام الحماية
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets["MY_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. قراءة الملف
if not os.path.exists("quran.txt"):
    st.error("❌ ملف quran.txt غير موجود.")
    st.stop()

with open("quran.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# 3. إعداد الـ API والموديل (التعديل هنا)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# مصفوفة الوكلاء
agents = {
    "وكيل الجمع 📚": "أنت وكيل الجمع المادي. استخرج الآيات المطلوبة فقط.",
    "وكيل النقد ⚖️": "أنت المحقق الصارم. حلل النص منطقياً."
}

agent_choice = st.sidebar.selectbox("الوكيل:", list(agents.keys()))

# محاولة الاتصال بالموديل الصحيح
try:
    model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=agents[agent_choice])
except:
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=agents[agent_choice])

# 4. واجهة الشات
st.title(f"💬 {agent_choice}")
st.success("✅ البينة جاهزة.")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("اسأل الوكيل..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    try:
        with st.chat_message("assistant"):
            response = model.generate_content(f"النص المرجعي:\n{full_text}\n\nالطلب: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"خطأ في الاستجابة: {e}")

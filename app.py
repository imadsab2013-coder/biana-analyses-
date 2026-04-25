import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

# إعدادات المختبر
st.set_page_config(page_title="مختبر البينة - Chat System", layout="wide")

# 1. نظام الحماية (123456)
if "password_correct" not in st.session_state:
    st.title("🔒 الدخول للمختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets["MY_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. تحميل البيانات المرجعية تلقائياً
@st.cache_resource
def load_data():
    if os.path.exists("quran.pdf"):
        reader = PdfReader("quran.pdf")
        return "".join([p.extract_text() for p in reader.pages if p.extract_text()])
    return None

full_text = load_data()

# 3. إدارة حالة الشات والوكلاء
if "messages" not in st.session_state: st.session_state.messages = []
if "shared_data" not in st.session_state: st.session_state.shared_data = ""

# القائمة الجانبية للتحكم
st.sidebar.title("🤖 غرفة التحكم")
agent_choice = st.sidebar.selectbox(
    "اختر الوكيل النشط:",
    ["وكيل الجمع 📚", "وكيل التحليل المنطقي 🔬", "وكيل الملاحظات والقواعد 🧩"]
)

# تحديد بروتوكول الوكيل
if agent_choice == "وكيل الجمع 📚":
    instr = "أنت وكيل الجمع. وظيفتك استخراج الآيات المتشابهة بدقة مادية من النص. لا تفسر، فقط اجمع."
elif agent_choice == "وكيل التحليل المنطقي 🔬":
    instr = "أنت وكيل التحليل. وظيفتك نقد النصوص بالمنطق والسبب والنتيجة بدون حشو أو خيال."
else:
    instr = "أنت وكيل القواعد. وظيفتك تثبيت القواعد المستخرجة وفحص صحة الملاحظات بناءً على الكتاب."

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=instr)

# 4. واجهة الشات
st.title(f"💬 {agent_choice}")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال الشات
if prompt := st.chat_input("تحدث مع الوكيل..."):
    # إذا كان هناك بيانات مشتركة من وكيل آخر، نضيفها للطلب
    input_text = f"سياق مشترك: {st.session_state.shared_data}\n\nسؤال المستخدم: {prompt}" if st.session_state.shared_data else prompt
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(f"النص المرجعي:\n{full_text}\n\nالطلب:\n{input_text}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # أزرار التحويل بين الوكلاء
        col1, col2 = st.columns(2)
        if col1.button("📤 تحويل النتيجة لوكيل التحليل"):
            st.session_state.shared_data = response.text
            st.success("تم تمرير البيانات لوكيل التحليل.")
        if col2.button("🧩 حفظ كقاعدة تحليل"):
            st.session_state.shared_data = response.text
            st.info("تم تثبيت هذه النتيجة كقاعدة للوكلاء الآخرين.")

# زر لمسح الشات والبدء من جديد
if st.sidebar.button("🗑️ مسح الجلسة"):
    st.session_state.messages = []
    st.session_state.shared_data = ""
    st.rerun()

import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="محلل البينة - المختبر المتكامل", layout="wide")

# 1. نظام الحماية (كود المختبر: 123456)
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets["MY_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. تحميل الملف (تم ضبطه على quran.txt)
@st.cache_resource
def load_data():
    file_path = "quran.txt" 
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 3. إدارة الذاكرة والتنقل بين الوكلاء
if "messages" not in st.session_state: st.session_state.messages = []
if "shared_context" not in st.session_state: st.session_state.shared_context = ""
if "fixed_rules" not in st.session_state: st.session_state.fixed_rules = ""

# 4. تعريف الوكلاء المتخصصين
agents_registry = {
    "وكيل الجمع 📚": "مهمتك استخراج وجمع كل الآيات المتشابهة أو الكلمات المرتبطة بالطلب من النص المرفق فقط. لا تفسير، لا وعظ، فقط اجمع البينة المادية.",
    "وكيل التحليل المنطقي 🔬": "وظيفتك نقد النصوص بالمنطق المادي (سبب ونتيجة). يمنع الحشو والخيال. اعتمد فقط على المكتوب في النص.",
    "وكيل النقد الصارم ⚖️": "أنت المحقق الصارم. ابحث عن الثغرات المنطقية، التناقضات الظاهرية، واختبر اتساق النص بأقصى درجات القسوة المنطقية.",
    "وكيل الملاحظات والقواعد 🧩": "مهمتك تثبيت القواعد المستخرجة من التحليلات السابقة وفحص صحة الملاحظات بناءً على البينة."
}

st.sidebar.title("🤖 غرفة التحكم")
agent_choice = st.sidebar.selectbox("اختر الوكيل النشط:", list(agents_registry.keys()))

system_p = agents_registry[agent_choice]
if st.session_state.fixed_rules:
    system_p += f"\n⚠️ قواعد العمل المثبتة: {st.session_state.fixed_rules}"

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro', system_instruction=system_p)

# 5. واجهة الشات
st.title(f"💬 {agent_choice}")
if not full_text: 
    st.error("⚠️ لم يتم العثور على الملف quran.txt. تأكد من رفعه في GitHub بنفس الاسم.")
else:
    st.success("✅ البينة المرجعية (quran.txt) جاهزة للتحليل.")

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("تحدث مع الوكيل..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        context_input = f"سياق محول: {st.session_state.shared_context}\n\nالطلب: {prompt}" if st.session_state.shared_context else prompt
        response = model.generate_content(f"النص المرجعي:\n{full_text}\n\n{context_input}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
        # أزرار التحويل الديناميكي
        col1, col2, col3 = st.columns(3)
        if col1.button("📤 تحويل للوكلاء"):
            st.session_state.shared_context = response.text
            st.toast("تم تمرير البيانات لوكيل آخر")
        if col2.button("🧩 تثبيت كقاعدة"):
            st.session_state.fixed_rules += f"\n- {response.text}"
            st.toast("تمت الإضافة لقواعد المختبر")
        if col3.button("🗑️ مسح الشات"):
            st.session_state.messages = []
            st.rerun()

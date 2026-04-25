import streamlit as st
import google.generativeai as genai
import os

# إعدادات واجهة المختبر
st.set_page_config(page_title="محلل البينة - المختبر المتكامل", layout="wide")

# 1. نظام الحماية (الباسورد)
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المختبر")
    pwd = st.text_input("كود المختبر", type="password")
    if st.button("فتح"):
        if pwd == st.secrets.get("MY_PASSWORD", "123456"):
            st.session_state["password_correct"] = True
            st.rerun()
    st.stop()

# 2. تحميل ملف النص المرجعي (quran.txt)
@st.cache_resource
def load_data():
    # البحث عن أي ملف نصي متاح في المستودع
    for name in ["quran.txt", "quran-simple.txt"]:
        if os.path.exists(name):
            with open(name, "r", encoding="utf-8") as f:
                return f.read()
    return None

full_text = load_data()

# 3. غرفة التحكم الجانبية (Sidebar)
st.sidebar.title("⚙️ غرفة التحكم")

# اختيار المحرك
ai_provider = st.sidebar.selectbox("اختر المحرك (AI Provider):", ["Google Gemini", "Claude AI (قريباً)"])

# اختيار الوكيل النشط
agents = {
    "وكيل الجمع 📚": "مهمتك استخراج الآيات المرتبطة بالطلب من النص المرفق فقط بدون أي زيادة.",
    "وكيل النقد الصارم ⚖️": "أنت المحقق الصارم. ابحث عن الثغرات والاتساق المنطقي في النصوص المرفقة.",
    "محلل البينة 🔬": "تقديم تحليل مادي شامل بناءً على قواعد السبب والنتيجة."
}
agent_choice = st.sidebar.selectbox("اختر الوكيل النشط:", list(agents.keys()))

# 4. تفعيل المحرك والـ API
model = None
if ai_provider == "Google Gemini":
    # خانة إدخال API Key يدوياً (لحل مشاكل الربط)
    user_api_key = st.sidebar.text_input("أدخل API Key يدوياً (اختياري):", type="password")
    final_key = user_api_key if user_api_key else st.secrets.get("GOOGLE_API_KEY")
    
    if final_key:
        genai.configure(api_key=final_key)
        try:
            # محاولة استخدام أحدث نسخة من موديل فلاش
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=agents[agent_choice])
        except:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
    else:
        st.sidebar.warning("⚠️ يرجى إدخال مفتاح API لبدء العمل.")

# 5. واجهة الشات والتحليل
st.title(f"💬 {agent_choice}")

if full_text:
    st.success("✅ البينة المرجعية (النص) محملة وجاهزة.")
else:
    st.error("❌ ملف النصوص (quran.txt) غير موجود في GitHub.")

# ذاكرة الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# استقبال الطلبات
if prompt := st.chat_input("أدخل تساؤلك للمختبر المادي..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if model and full_text:
        with st.chat_message("assistant"):
            try:
                # دمج النص المرجعي مع الطلب لضمان دقة المحرك
                full_prompt = f"النص المرجعي:\n{full_text}\n\nالمهمة المطلوبة: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ في استجابة المحرك: {e}")
    else:
        st.info("💡 تأكد من اختيار المحرك وإدخال الـ API Key في القائمة الجانبية.")

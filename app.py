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

# 2. تحميل ملف البيانات (quran.txt)
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 3. غرفة التحكم الجانبية
st.sidebar.title("⚙️ غرفة التحكم")

# اختيار المحرك (هنا يمكنك التبديل مستقبلاً)
ai_provider = st.sidebar.selectbox("اختر المحرك (AI Provider):", ["Google Gemini", "Claude AI (قريباً)"])

# اختيار الوكيل المتخصص
agents = {
    "وكيل الجمع 📚": "مهمتك استخراج الآيات المرتبطة بالطلب من النص المرفق فقط.",
    "وكيل النقد الصارم ⚖️": "أنت المحقق الصارم. ابحث عن الثغرات المنطقية في النص.",
    "محلل البينة 🔬": "تحليل شامل بناءً على قواعد المنطق والسبب والنتيجة."
}
agent_choice = st.sidebar.selectbox("اختر الوكيل النشط:", list(agents.keys()))

# 4. تفعيل المحرك المختار (Google Gemini حالياً)
model = None
if ai_provider == "Google Gemini":
    # خانة يدوية لوضع API Key إذا أردت استخدامه مباشرة في الموقع
    user_api_key = st.sidebar.text_input("أدخل API Key يدوياً (اختياري):", type="password")
    final_key = user_api_key if user_api_key else st.secrets.get("GOOGLE_API_KEY")
    
    if final_key:
        genai.configure(api_key=final_key)
        try:
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=agents[agent_choice])
        except:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
    else:
        st.warning("⚠️ يرجى ربط الـ API Key في Secrets أو إدخاله يدوياً.")

# 5. واجهة الشات
st.title(f"💬 {agent_choice}")
if full_text:
    st.success("✅ البينة المرجعية (quran.txt) جاهزة.")
else:
    st.error("❌ ملف quran.txt غير موجود في GitHub.")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("أدخل تساؤلك للمختبر..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    if model:
        with st.chat_message("assistant"):
            try:
                full_prompt = f"النص المرجعي:\n{full_text}\n\nالمهمة: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطأ في المحرك: {e}")
    else:
        st.error("❌ لا يمكن بدء التحليل بدون مفتاح API مفعل.")

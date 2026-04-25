import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة والجمالية
st.set_page_config(page_title="مختبر محلل البينة", page_icon="🔬", layout="wide")

# تخصيص المظهر بالـ CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    .stTextInput>div>div>input { color: #262730; }
    </style>
    """, unsafe_allow_html=True)

# 2. نظام الحماية
if "password_correct" not in st.session_state:
    st.title("🔒 دخول المصرح لهم فقط")
    pwd = st.text_input("كود المختبر (Password)", type="password")
    if st.button("فتح البوابة"):
        if pwd == st.secrets["MY_PASSWORD"]:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("⚠️ كود خاطئ. الدخول ممنوع.")
    st.stop()

# 3. إعدادات الوكلاء (Agents)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("🤖 غرفة التحكم بالوكلاء")

agent_type = st.sidebar.selectbox(
    "اختر الوكيل المتخصص:",
    ["وكيل فحص التناقضات ⚖️", "وكيل الاستدلال المادي 🔎", "وكيل نقد المتون 🧩"]
)

# تحديد بروتوكول الوكيل المختار
if agent_type == "وكيل فحص التناقضات ⚖️":
    instruction = "أنت وكيل متخصص في كشف التناقضات. مهمتك مقارنة النصوص ببعضها واستخراج أي تضارب منطقي مادي."
elif agent_type == "وكيل الاستدلال المادي 🔎":
    instruction = "أنت وكيل مادي. تركز فقط على الأرقام، الأماكن، الزمان، والأدلة الحسية المذكورة في النص."
else:
    instruction = "أنت وكيل نقد المتون. تفحص النص بناءً على قواعد المنطق الصارم والسبب والنتيجة."

# 4. تشغيل المحرك
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(model_name='gemini-1.5-pro', system_instruction=instruction)

# 5. الواجهة الرئيسية
st.title("🔬 مختبر محلل البينة - التحليل المادي")
st.info(f"🟢 الوكيل النشط حالياً: {agent_type}")

uploaded_file = st.file_uploader("📥 ارفع المادة الخام للتحليل (PDF)", type="pdf")

if uploaded_file:
    with st.status("⏳ جاري سحب البيانات من الملف..."):
        reader = PdfReader(uploaded_file)
        full_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
        st.write(f"✅ تم سحب {len(reader.pages)} صفحة.")

    st.markdown("---")
    query = st.text_area("💬 ما هي المهمة المطلوبة من الوكيل؟", placeholder="مثال: هل هناك تناقض بين ما ورد في المقدمة وما ورد في الخاتمة؟")

    if st.button("🚀 بدء التشغيل"):
        if query:
            with st.spinner("🧠 الوكيل يقوم بمعالجة البيانات..."):
                response = model.generate_content(f"بناءً على البينة التالية:\n{full_text}\n\nأجب على التالي بالمنطق المادي: {query}")
                st.subheader("📝 تقرير الوكيل النهائي:")
                st.markdown(response.text)
                
                # إضافة زر لتحميل التقرير
                st.download_button("📥 تحميل التقرير", response.text, file_name="analysis_report.txt")
        else:
            st.warning("⚠️ يرجى تزويد الوكيل بمهمة محددة.")

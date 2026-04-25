import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="محلل البينة", layout="wide")

# نظام الحماية
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 الدخول للمختبر")
        pwd = st.text_input("أدخل كلمة السر", type="password")
        if st.button("دخول"):
            if pwd == st.secrets["MY_PASSWORD"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("كلمة سر خاطئة")
        return False
    return True

if check_password():
    st.sidebar.success("متصل بالوكلاء")
    st.title("🔬 محلل البينة - التحليل المادي")
    
    # ربط الذكاء الاصطناعي
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    uploaded_file = st.file_uploader("ارفع البينة (PDF)", type="pdf")
    
    if uploaded_file:
        st.info("تم رفع الملف. نحن الآن بصدد بناء الوكلاء المتخصصين.")
        query = st.text_input("ما الذي تريد استخراجه بالمنطق المادي؟")
        if query:
            st.write("جاري التحليل...")

import streamlit as st
import google.generativeai as genai

st.title("🔬 مختبر البينة (الربط المباشر)")

# 1. جلب المفتاح
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # إعداد بسيط وقوي
        genai.configure(api_key=api_key)
        
        # استخدام اسم الموديل بدون أي إضافات (هذا المسار هو الأكثر استقراراً)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # محاولة توليد محتوى بسيط جداً
        response = model.generate_content("سلام")
        
        st.success("🟢 اشتغل! البينة ظهرت")
        st.write("رد الـ AI:", response.text)
        
    except Exception as e:
        # إذا استمر المشكل، سنغير "الموديل" نفسه داخل الكود
        st.error(f"🔴 عطل مادي: {e}")
        st.info("💡 جرب تبدل 'gemini-1.5-flash' بـ 'gemini-pro' في الكود إذا بقى الـ 404.")
else:
    st.error("❌ المفتاح غير موجود في السكرت (Secrets)")

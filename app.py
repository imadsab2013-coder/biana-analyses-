import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.title("🔬 مختبر البينة (المسار المستقر)")

# جلب المفتاح
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # إعداد الإرسال ليكون مستقراً ومباشراً
        genai.configure(api_key=api_key)
        
        # الحل القاطع: استخدام RequestOptions لإجبار السيرفر على v1
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            "سلام، هل المحرك شغال؟",
            request_options=RequestOptions(api_version='v1') # إجبار النسخة V1
        )
        
        st.success("🟢 تم كسر الحصار! المحرك شغال")
        st.write("الرد:", response.text)
        
    except Exception as e:
        st.error(f"🔴 عطل تقني: {e}")
        st.info("💡 إذا استمر الـ 404، جرب تبدل 'gemini-1.5-flash' بـ 'gemini-pro'")
else:
    st.error("❌ المفتاح مفقود في Secrets")

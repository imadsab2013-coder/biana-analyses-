import streamlit as st
import google.generativeai as genai

# الربط المباشر والواضح
st.title("🧪 فحص محرك البينة")

if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    try:
        # محاولة الاتصال بأبسط موديل
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("سلام")
        st.success("🟢 الـ AI خدام!")
        st.write("الرد:", response.text)
    except Exception as e:
        st.error(f"🔴 الـ AI محبوس بسباب: {e}")
else:
    st.warning("⚪ السيرفر ما شايفش المفتاح (Secrets خاوية)")

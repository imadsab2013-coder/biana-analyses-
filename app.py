import streamlit as st
import google.generativeai as genai

st.title("🧪 فحص محرك البينة (المسار المستقر)")

# جلب المفتاح من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    try:
        # الحل السحري: إجبار المكتبة على تجاهل v1beta واستخدام البروتوكول المستقر
        genai.configure(api_key=api_key, transport='rest')
        
        # استدعاء الموديل بالاسم القصير لتفادي خلط المسارات
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # تجربة الاتصال
        response = model.generate_content("سلام")
        
        st.success("🟢 البولة خضراء: المحرك شغال بنجاح!")
        st.write("الرد من المحرك:", response.text)
        
    except Exception as e:
        # إذا استمر الخطأ، سنعرضه بدقة للتشخيص
        st.error(f"🔴 فشل الاتصال: {e}")
        st.info("💡 إذا ظهر خطأ 404، جرب كتابة 'gemini-pro' بدلاً من 'gemini-1.5-flash' في الكود.")
else:
    st.error("❌ المفتاح غير موجود في Settings (Secrets)")

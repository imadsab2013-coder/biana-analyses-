import streamlit as st
import requests

st.set_page_config(page_title="مختبر البينة", layout="centered")
st.title("🔬 مختبر البينة (Qwen 2.5)")

# جلب المفتاح بشكل آمن وتصفيته من أي فراغات
api_key = st.secrets.get("OPENROUTER_API_KEY", "").strip()

if api_key:
    # واجهة بسيطة للتحدث مع Qwen
    user_input = st.chat_input("حلل بالمنطق الصيني...")
    
    if user_input:
        st.chat_message("user").write(user_input)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "alibaba/qwen-2-7b-instruct:free",
            "messages": [{"role": "user", "content": user_input}]
        }
        
        with st.spinner("جاري استحضار البينة..."):
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                if response.status_code == 200:
                    result = response.json()['choices'][0]['message']['content']
                    st.chat_message("assistant").write(result)
                else:
                    st.error(f"🔴 عطل في المحرك: {response.status_code}")
            except Exception as e:
                st.error(f"🔴 خطأ مادي: {e}")
else:
    st.warning("⚠️ البينة ناقصة: الساروت (API Key) غير موجود في Secrets.")

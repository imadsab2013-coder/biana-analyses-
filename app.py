import streamlit as st
import requests

st.set_page_config(page_title="مختبر البينة", layout="centered")
st.title("🔬 مختبر البينة")

# جلب المفتاح وتصفيته
api_key = st.secrets.get("OPENROUTER_API_KEY", "").strip()

if api_key:
    if prompt := st.chat_input("حلل بالمنطق..."):
        st.chat_message("user").write(prompt)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://streamlit.io",
            "Content-Type": "application/json"
        }
        
        # استخدمنا هذا الموديل لأنه الأكثر استقراراً للمجاني حالياً
        payload = {
            "model": "google/gemma-2-9b-it:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        with st.spinner("جاري استحضار البينة..."):
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.chat_message("assistant").write(answer)
                else:
                    st.error(f"🔴 عطل {response.status_code}. جرب كتابة 'test' للتأكد.")
                    st.write("تفاصيل الخطأ:", response.text)
            except Exception as e:
                st.error(f"🔴 خطأ مادي: {e}")
else:
    st.warning("⚠️ المفتاح (API Key) غير موجود في Secrets.")

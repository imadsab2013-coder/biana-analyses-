import streamlit as st
import requests

st.title("🔬 مختبر البينة (Qwen 2.5)")

# جلب المفتاح وتصفيته بدقة
api_key = st.secrets.get("OPENROUTER_API_KEY", "").strip()

if api_key:
    user_input = st.chat_input("حلل بالمنطق...")
    if user_input:
        st.chat_message("user").write(user_input)
        
        # بروتوكول الاتصال الصحيح
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://streamlit.io", # ضروري لبعض الموديلات
            "Content-Type": "application/json"
        }
        
        # استخدام الموديل المجاني المستقر
        payload = {
            "model": "alibaba/qwen-2-7b-instruct:free",
            "messages": [{"role": "user", "content": user_input}]
        }
        
        with st.spinner("جاري استنطاق المحرك..."):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    answer = response.json()['choices'][0]['message']['content']
                    st.chat_message("assistant").write(answer)
                else:
                    st.error(f"🔴 خطأ {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"🔴 عطل تقني: {e}")
else:
    st.warning("⚠️ الساروت (API Key) مفقود في الإعدادات.")

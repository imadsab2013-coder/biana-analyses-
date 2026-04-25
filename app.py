import streamlit as st
import requests

st.title("🔬 مختبر البينة (Qwen 2.5)")

# جلب المفتاح من Secrets
api_key = st.secrets.get("OPENROUTER_API_KEY")

if api_key:
    try:
        # محاولة تواصل بسيطة مع Qwen
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "alibaba/qwen-2.5-72b-instruct",
                "messages": [{"role": "user", "content": "سلام"}]
            }
        )
        
        if response.status_code == 200:
            res_text = response.json()['choices'][0]['message']['content']
            st.success("🟢 اشتعل! البينة ظهرت")
            st.write("رد Qwen:", res_text)
        else:
            st.error(f"🔴 خطأ في المحرك: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error(f"🔴 عطل مادي: {e}")
else:
    st.error("❌ المفتاح غير موجود في السكرت (Secrets)")

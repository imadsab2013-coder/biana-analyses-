import streamlit as st
import requests

st.title("🔬 مختبر البينة (Qwen 2.5)")

api_key = st.secrets.get("OPENROUTER_API_KEY", "").strip()

if api_key:
    user_input = st.chat_input("حلل بالمنطق...")
    if user_input:
        st.chat_message("user").write(user_input)
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "qwen/qwen-2-7b-instruct:free",
            "messages": [{"role": "user", "content": user_input}]
        }
        
        try:
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            if response.status_code == 200:
                answer = response.json()['choices'][0]['message']['content']
                st.chat_message("assistant").write(answer)
            else:
                st.error(f"عطل في المحرك: {response.text}")
        except Exception as e:
            st.error(f"خطأ مادي: {e}")
else:
    st.warning("أدخل الساروت في Secrets")

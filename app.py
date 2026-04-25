import streamlit as st
import requests

st.set_page_config(page_title="مختبر البينة", layout="wide")
st.title("🔬 مختبر البينة (Qwen 2.5)")

# جلب المفتاح وتصفيته
api_key = st.secrets.get("OPENROUTER_API_KEY", "").strip()

if api_key:
    # واجهة الدردشة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("حلل بالمنطق..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit.io"
        }
        
        # هاد الموديل هو اللي خدام فابور دابا 100%
        payload = {
            "model": "qwen/qwen-2-7b-instruct:free", 
            "messages": st.session_state.messages
        }
        
        with st.spinner("جاري استحضار البينة..."):
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                if response.status_code == 200:
                    full_response = response.json()['choices'][0]['message']['content']
                    with st.chat_message("assistant"):
                        st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error(f"خطأ {response.status_code}: الموديل غير متاح حالياً.")
                    # اختياري: كود باش تعرف اشنو هما الموديلات اللي خدامين دابا
                    st.info("جرب تبديل اسم الموديل في الكود لـ: google/gemma-2-9b-it:free")
            except Exception as e:
                st.error(f"عطل مادي: {e}")
else:
    st.warning("⚠️ البينة ناقصة: الساروت (API Key) غير موجود في Secrets.")

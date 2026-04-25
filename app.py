import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="مختبر البينة", layout="wide")

# 1. تحميل النص المرجعي
@st.cache_resource
def load_data():
    if os.path.exists("quran.txt"):
        with open("quran.txt", "r", encoding="utf-8") as f:
            return f.read()
    return None

full_text = load_data()

# 2. الإعدادات الجانبية
st.sidebar.title("⚙️ الإعدادات المادية")

models_dict = {
    "Gemini 1.5 Flash": "models/gemini-1.5-flash",
    "Gemini 1.5 Pro": "models/gemini-1.5-pro",
    "Gemini 2.0 Flash": "models/gemini-2.0-flash-exp"
}

version_label = st.sidebar.selectbox("اختر النسخة:", list(models_dict.keys()))
model_path = models_dict[version_label]

api_key = st.secrets.get("GOOGLE_API_KEY")

# --- نظام "البولة" (Connection Indicator) ---
connection_status = False
if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name

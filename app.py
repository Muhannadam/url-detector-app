import streamlit as st
import pandas as pd
import joblib
import urllib.request
import os
import re

# تحميل النموذج من Google Drive مرة واحدة فقط
model_path = "random_forest_url_model.pkl"
if not os.path.exists(model_path):
    file_id = "11XOMMCrE8IKd8lRhra3dGyTlLv2RQJsn"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    urllib.request.urlretrieve(url, model_path)

# تحميل النموذج والميزات
model = joblib.load("random_forest_url_model.pkl")
columns = joblib.load("feature_columns.pkl")

# استخراج الميزات من الرابط
def extract_features(url):
    return {
        'url_length': len(url),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_slashes': url.count('/'),
        'has_ip': int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))),
        'has_https': int('https' in url),
        'has_at_symbol': int('@' in url),
        'num_digits': sum(c.isdigit() for c in url),
        'suspicious_words': int(any(w in url.lower() for w in ['login', 'verify', 'update', 'secure', 'account']))
    }

# واجهة Streamlit
st.title("🔐 Malicious URL Detector")
st.markdown("تحقق من أي رابط باستخدام نموذج الذكاء الاصطناعي المدرب 👇")

url = st.text_input("أدخل الرابط هنا:")

if url:
    features = pd.DataFrame([extract_features(url)], columns=columns)
    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]

    if pred == 1:
        st.error(f"⚠️ النتيجة: الرابط **خبيث** بنسبة {prob:.2%}")
    else:
        st.success(f"✅ النتيجة: الرابط **سليم** بنسبة {1 - prob:.2%}")


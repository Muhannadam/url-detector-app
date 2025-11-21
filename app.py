import streamlit as st
import pandas as pd
import joblib
import urllib.request
import os
import re

# تحميل النموذج من Google Drive مرة واحدة فقط
MODEL_PATH = "random_forest_url_model.pkl"
FEATURES_PATH = "feature_columns.pkl"
GDRIVE_FILE_ID = "11XOMMCrE8IKd8lRhra3dGyTlLv2RQJsn"

if not os.path.exists(MODEL_PATH):
    url = f"https://drive.google.com/uc?export=download&id={GDRIVE_FILE_ID}"
    urllib.request.urlretrieve(url, MODEL_PATH)

# تحميل النموذج وملف الأعمدة
model = joblib.load(MODEL_PATH)
columns = joblib.load(FEATURES_PATH)

# دالة استخراج الميزات من الرابط
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

# واجهة رئيسية
st.set_page_config(page_title="AI Malicious URL Detector", layout="centered", page_icon="🛡️")

st.title("🛡️ AI-based Malicious URL Detector")
st.markdown("تحقق من الروابط باستخدام نموذج ذكي مدرب للكشف عن المواقع المشبوهة.")

# تبويبات: فحص الرابط / معلومات
tab1, tab2 = st.tabs(["🔎 تحقق من رابط", "ℹ️ حول المشروع"])

# ========== التبويب 1 ==========
with tab1:
    st.subheader("🚨 أدخل الرابط المراد فحصه:")
    url = st.text_input("مثال: https://secure-login.example.com/account")

    if url:
        features = pd.DataFrame([extract_features(url)], columns=columns)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        if prediction == 1:
            st.error(f"⚠️ هذا الرابط مصنف كـ **خبيث** بنسبة {probability:.2%}")
        else:
            st.success(f"✅ هذا الرابط **سليم** بنسبة {1 - probability:.2%}")

        # عرض الميزات المستخرجة
        with st.expander("📊 الميزات المستخرجة من الرابط"):
            st.write(features.T.rename(columns={0: "القيمة"}))

# ========== التبويب 2 ==========
with tab2:
    st.subheader("ℹ️ حول هذا المشروع")
    st.markdown("""
هذا النظام يستخدم تقنيات تعلم الآلة للكشف عن الروابط المشبوهة بناءً على ميزات مثل:
- وجود كلمات مشبوهة مثل: `login`, `verify`, `secure`
- طول الرابط وعدد الرموز الخاصة
- وجود عنوان IP ضمن الرابط
- غياب أو وجود بروتوكول HTTPS

### 🧠 معلومات عن النموذج:
- **الخوارزمية:** Random Forest Classifier
- **الدقة:** 92%
- **AUC:** 0.96
- **نوع المشروع:** مشروع جامعي لمقرر EMAI-644: AI for Cybersecurity - Fall 2025

### 📁 الملفات المستخدمة:
- `random_forest_url_model.pkl`: النموذج المدرب
- `feature_columns.pkl`: أسماء الأعمدة المستخدمة في التدريب

---

تم تطوير هذا المشروع بواسطة **Muhannad Almuntashiri**  
[LinkedIn](https://www.linkedin.com) | [GitHub](https://github.com)
    """)

---

## ✅ التعليمات التالية:

1. احفظ هذا الكود باسم `app.py`
2. تأكد أن لديك الملفات:
   - `feature_columns.pkl` (ارفعه مع الريبو في GitHub)
   - `random_forest_url_model.pkl` محفوظ في Google Drive
3. ارفع المشروع إلى GitHub
4. انشره عبر [Streamlit Cloud](https://streamlit.io/cloud)

---

هل ترغب أن أرسل لك المشروع كـ `.zip` جاهز للرفع؟  
أو أساعدك في تصميم شعار أو صفحة `About` مرئية أكثر؟

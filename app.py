import streamlit as st
import pandas as pd
import joblib
import urllib.request
import os
import re

# تحميل النموذج من Google Drive
MODEL_PATH = "random_forest_url_model.pkl"
FEATURES_PATH = "feature_columns.pkl"
GDRIVE_FILE_ID = "11XOMMCrE8IKd8lRhra3dGyTlLv2RQJsn"

# أضف هذا الديكوريتور (Decorator) فوق دالة التحميل
@st.cache_resource
def load_model_and_columns():
    if not os.path.exists(MODEL_PATH):
        url = f"https://drive.google.com/uc?export=download&id={GDRIVE_FILE_ID}"
        urllib.request.urlretrieve(url, MODEL_PATH)
    
    _model = joblib.load(MODEL_PATH)
    _columns = joblib.load(FEATURES_PATH)
    return _model, _columns

# استدعاء الدالة
model, columns = load_model_and_columns()

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

# إعداد واجهة التطبيق
st.set_page_config(page_title="اكتشاف الروابط الضارة بالذكاء الاصطناعي", layout="centered", page_icon="🛡️")

# CSS لدعم RTL
st.markdown("""
    <style>
    body, .main, .stApp {
        direction: rtl;
        text-align: right;
    }
    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        float: right;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("التعرف على الروابط المشبوهة باستخدام الذكاء الاصطناعي")
st.markdown("تحقق من الروابط المشكوك فيها باستخدام نموذج مدرّب للتصنيف الذكي.")

# التبويبات
tab1, tab2 = st.tabs(["تحقق من رابط", "حول المشروع"])

# التبويب الأول
with tab1:
    
    st.subheader("أدخل الرابط المراد فحصه:")
    url = st.text_input("")

    if url:
        features = pd.DataFrame([extract_features(url)], columns=columns)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        if prediction == 1:
            st.error(f"هذا الرابط **خبيث**")
        else:
            st.success(f"هذا الرابط **سليم**")

        # عرض الميزات المستخرجة
        with st.expander("التفاصيل التقنية للرابط"):
            st.write(features.T.rename(columns={0: "القيمة"}))

            # عرض أهم أسباب التصنيف (أهم الميزات)
        with st.expander("ما السبب وراء هذا التصنيف؟"):
            importances = model.feature_importances_
            feature_values = features.iloc[0]
            # حساب الدرجات الأولية
            raw_scores = {
                col: importances[i] * abs(feature_values[col])
                for i, col in enumerate(columns)
            }
            
            # مجموع الدرجات
            total = sum(raw_scores.values())
            
            # التطبيع بحيث يصبح المجموع = 1
            normalized_scores = {
                col: (score / total) if total != 0 else 0
                for col, score in raw_scores.items()
            }
            
            # ترتيب الميزات
            sorted_scores = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

            for name, score in sorted_scores[:3]:
                st.write(f"- `{name}` ساهم بنسبة تقريبية: {score:.2%}")



# التبويب الثاني
with tab2:
    st.subheader("حول هذا الموقع")
    st.markdown("""
تم بناء هذا النظام لاكتشاف الروابط الضارة باستخدام خوارزميات تعلم الآلة. يعتمد على استخراج ميزات مهمة من الرابط مثل:

- وجود كلمات حساسة مثل `login`, `verify`, `secure` وغيرها
- الطول وعدد الرموز الخاصة
- وجود IP أو عدم وجود HTTPS
- وغيرها من الخصائص

---

### معلومات عن النموذج:
- **الخوارزمية:** Random Forest
- **الدقة:** 92%
- **AUC:** 0.96
- مشروع جامعي لمقرر EMAI-644 - مقرر الذكاء الاصناعي في الآمن السيبراني

---

تم تطويره بواسطة: **مهنّد المنتشري**  
[GitHub](https://github.com/Muhannadam/url-detector-app/blob/main/README.md)
""")

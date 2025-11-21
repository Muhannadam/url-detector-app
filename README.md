# 🛡️ Arabic AI-Powered Malicious URL Detector

A bilingual (Arabic-first) web application built with **Streamlit** that intelligently detects whether a given URL is malicious or benign using a trained **Random Forest Classifier**.

> 💡 Powered by handcrafted features extracted from raw URLs + an ML model trained on thousands of phishing and benign links.

---

## 🚀 Live Demo

🖥️ [Launch the App on Streamlit Cloud](https://malicious-url-detector.streamlit.app/)  
Paste any URL and instantly get a prediction.

---

## 🔍 Key Features

- ✅ **Arabic-first interface with RTL support**
- 📎 Extracts 9 handcrafted features from the input URL
- 🧠 Uses a trained **Random Forest** model with 92% accuracy (AUC = 0.96)
- 🔐 Designed for cybersecurity education and awareness
- 💬 Explains prediction with top 3 contributing features ("Why was this classified as malicious?")
- 📊 Includes technical breakdown per input

---

## 🧠 Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Input features**:
  - URL length
  - Number of dots, hyphens, slashes
  - Presence of IP address
  - Use of HTTPS
  - Suspicious keywords (`login`, `verify`, etc.)
  - Use of `@` symbol
  - Number of digits
- **Trained on**: A balanced phishing URL dataset (upsampled)

The trained model is hosted on **Google Drive** and auto-loaded on first run.

---

## 📁 Project Structure


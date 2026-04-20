import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import streamlit as st

st.set_page_config(
    page_title="Deteksi Emosi Pelanggan",
    page_icon="💬",
    layout="wide"
)

st.write("🚀 App starting...")

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_my_model():
    import tensorflow as tf
    return tf.keras.models.load_model("model_emotion.keras", compile=False)

@st.cache_resource
def load_tokenizer():
    import pickle
    with open("tokenizer.pkl", "rb") as f:
        return pickle.load(f)

st.write("⏳ Loading model...")
model = load_my_model()
tokenizer = load_tokenizer()
st.success("✅ Model Loaded!")

# =========================
# IMPORT
# =========================
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
from datetime import datetime
from tensorflow.keras.preprocessing.sequence import pad_sequences

# =========================
# LABEL (6 EMOSI)
# =========================
label_map = {
    0: "Marah",
    1: "Takut",
    2: "Senang",
    3: "Cinta",
    4: "Sedih",
    5: "Netral"
}

label_emoji = {
    0: "😠",
    1: "😨",
    2: "😊",
    3: "❤️",
    4: "😢",
    5: "😐"
}

max_length = 50

# =========================
# PREPROCESS
# =========================
def preprocess(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# =========================
# PREDICT (FIXED)
# =========================
def predict_emotion(text):
    clean = preprocess(text)
    seq = tokenizer.texts_to_sequences([clean])
    pad = pad_sequences(seq, maxlen=max_length, padding='post')
    pred = model.predict(pad, verbose=0)[0]
    result = int(np.argmax(pred))  # 🔥 FIX
    return result, pred

# =========================
# BATCH PREDICT
# =========================
def predict_batch(texts):
    cleaned = [preprocess(str(t)) for t in texts]
    seqs = tokenizer.texts_to_sequences(cleaned)
    pads = pad_sequences(seqs, maxlen=max_length, padding='post')
    preds = model.predict(pads, verbose=0)

    results = [int(np.argmax(p)) for p in preds]
    return results, preds

# =========================
# MENU
# =========================
st.markdown("## 📌 Menu")

col1, col2, col3, col4 = st.columns(4)

if "menu" not in st.session_state:
    st.session_state.menu = "prediksi"

with col1:
    if st.button("🔍 Prediksi"):
        st.session_state.menu = "prediksi"

with col2:
    if st.button("📦 Analisis Batch"):
        st.session_state.menu = "batch"

with col3:
    if st.button("📊 Evaluasi Model"):
        st.session_state.menu = "evaluasi"

with col4:
    if st.button("📁 Dataset"):
        st.session_state.menu = "dataset"

menu = st.session_state.menu

st.markdown("---")

# =========================
# 1. PREDIKSI
# =========================
if menu == "prediksi":

    st.title("💬 Deteksi Emosi Pelanggan")

    user_input = st.text_area("Masukkan teks:", height=120)

    if st.button("🔍 Analisis Emosi"):

        if user_input.strip() == "":
            st.warning("⚠️ Masukkan teks dulu!")
        else:
            result, pred = predict_emotion(user_input)

            col1, col2 = st.columns([1,2])

            with col1:
                label = label_map[result]
                emoji = label_emoji[result]

                if result == 0:
                    st.error(f"{emoji} {label}")
                elif result in [1,4]:
                    st.warning(f"{emoji} {label}")
                elif result in [2,3]:
                    st.success(f"{emoji} {label}")
                else:
                    st.info(f"{emoji} {label}")

            with col2:
                st.subheader("Probabilitas")
                for i in range(6):
                    st.write(f"{label_emoji[i]} {label_map[i]}: {round(pred[i]*100,1)}%")
                    st.progress(float(pred[i]))

# =========================
# 2. BATCH
# =========================
elif menu == "batch":

    st.title("📦 Analisis Batch")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)

        if st.button("Proses"):
            texts = df.iloc[:,0].tolist()
            results, preds = predict_batch(texts)

            df["emosi"] = [label_map[r] for r in results]

            st.success("Selesai!")

            counts = df["emosi"].value_counts()

            st.write("Distribusi Emosi")
            st.bar_chart(counts)

            st.dataframe(df)

# =========================
# 3. EVALUASI
# =========================
elif menu == "evaluasi":

    st.title("📊 Evaluasi Model")

    st.metric("Accuracy", "72.6%")

    cm = np.array([
        [47, 0, 11, 4, 0, 2],
        [0, 7, 0, 1, 0, 0],
        [2, 1, 207, 0, 0, 37],
        [0, 0, 3, 8, 1, 2],
        [4, 0, 2, 1, 7, 0],
        [3, 0, 46, 1, 0, 46]
    ])

    classes = list(label_map.values())

    fig, ax = plt.subplots()
    ax.imshow(cm)

    ax.set_xticks(range(6))
    ax.set_yticks(range(6))
    ax.set_xticklabels(classes, rotation=45)
    ax.set_yticklabels(classes)

    for i in range(6):
        for j in range(6):
            ax.text(j, i, cm[i,j], ha='center', va='center')

    st.pyplot(fig)

# =========================
# 4. DATASET
# =========================
elif menu == "dataset":

    st.title("📁 Dataset")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file:
        df = pd.read_csv(file)
        st.dataframe(df)
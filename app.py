import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import streamlit as st

# =========================
# PAGE CONFIG & CUSTOM CSS
# =========================
st.set_page_config(
    page_title="Deteksi Emosi Pelanggan",
    page_icon="💬",
    layout="wide"
)

st.markdown("""
<style>
    /* ─── Import Font ─── */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* ─── Root & Base ─── */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* ─── Background ─── */
    .stApp {
        background-color: #F7F8FA;
    }

    /* ─── Hide default header/footer ─── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ─── Top Banner ─── */
    .top-banner {
        background: linear-gradient(135deg, #1A56DB 0%, #3B82F6 100%);
        border-radius: 14px;
        padding: 28px 36px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .top-banner-icon {
        font-size: 40px;
        line-height: 1;
    }
    .top-banner-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .top-banner-sub {
        color: rgba(255,255,255,0.80);
        font-size: 13px;
        margin: 2px 0 0;
        font-weight: 400;
    }

    /* ─── Navigation Tabs ─── */
    .nav-bar {
        display: flex;
        gap: 8px;
        background: #ffffff;
        border-radius: 10px;
        padding: 6px;
        border: 1px solid #E5E7EB;
        margin-bottom: 28px;
    }
    .nav-btn {
        flex: 1;
        text-align: center;
        padding: 9px 14px;
        border-radius: 7px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        border: none;
        background: transparent;
        color: #6B7280;
        transition: all 0.18s;
    }
    .nav-btn.active {
        background: #1A56DB;
        color: #ffffff;
    }

    /* ─── Card ─── */
    .card {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        padding: 24px 28px;
        margin-bottom: 20px;
    }
    .card-title {
        font-size: 15px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 16px;
    }

    /* ─── Emotion Result ─── */
    .emotion-result {
        border-radius: 12px;
        padding: 22px 26px;
        text-align: center;
        margin-bottom: 16px;
    }
    .emotion-result.marah  { background: #FEF2F2; border: 1px solid #FECACA; }
    .emotion-result.takut  { background: #FFFBEB; border: 1px solid #FDE68A; }
    .emotion-result.senang { background: #F0FDF4; border: 1px solid #BBF7D0; }
    .emotion-result.cinta  { background: #FDF2F8; border: 1px solid #FBCFE8; }
    .emotion-result.sedih  { background: #EFF6FF; border: 1px solid #BFDBFE; }
    .emotion-result.netral { background: #F9FAFB; border: 1px solid #E5E7EB; }

    .emotion-emoji { font-size: 42px; margin-bottom: 6px; }
    .emotion-label {
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    .emotion-label.marah  { color: #DC2626; }
    .emotion-label.takut  { color: #D97706; }
    .emotion-label.senang { color: #16A34A; }
    .emotion-label.cinta  { color: #DB2777; }
    .emotion-label.sedih  { color: #2563EB; }
    .emotion-label.netral { color: #6B7280; }

    /* ─── Probability Bar ─── */
    .prob-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }
    .prob-label { font-size: 13px; color: #374151; width: 80px; }
    .prob-bar-bg {
        flex: 1;
        background: #F3F4F6;
        border-radius: 99px;
        height: 7px;
        overflow: hidden;
    }
    .prob-bar-fill {
        height: 100%;
        border-radius: 99px;
        background: #1A56DB;
    }
    .prob-pct { font-size: 12px; color: #6B7280; width: 40px; text-align: right; font-weight: 500; }

    /* ─── Metric Card ─── */
    .metric-box {
        background: #F0F5FF;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
        border: 1px solid #C7D7FF;
    }
    .metric-val { font-size: 28px; font-weight: 700; color: #1A56DB; }
    .metric-lbl { font-size: 12px; color: #6B7280; margin-top: 4px; }

    /* ─── Confusion Matrix ─── */
    .cm-title {
        font-size: 13px;
        font-weight: 600;
        color: #374151;
        margin-bottom: 12px;
    }

    /* ─── Section Heading ─── */
    .section-heading {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
        margin: 0 0 18px;
        padding-bottom: 12px;
        border-bottom: 2px solid #E5E7EB;
    }

    /* ─── Streamlit widget overrides ─── */
    .stTextArea textarea {
        border-radius: 10px !important;
        border-color: #D1D5DB !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 14px !important;
    }
    /* ─── Primary button: active nav tab & Analisis ─── */
    .stButton > button[kind="primaryFormSubmit"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #1A56DB !important;
        color: #ffffff !important;
        border: 1px solid #1A56DB !important;
        border-radius: 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 1px 6px rgba(26,86,219,0.22) !important;
    }
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #1348C0 !important;
        border-color: #1348C0 !important;
    }

    /* ─── Secondary button: inactive nav tabs ─── */
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #ffffff !important;
        color: #6B7280 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #F3F4F6 !important;
        color: #374151 !important;
        border-color: #D1D5DB !important;
    }

    div[data-testid="stAlert"] { border-radius: 10px !important; }
    .stProgress > div > div { background-color: #1A56DB !important; }
</style>
""", unsafe_allow_html=True)


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

with st.spinner("Memuat model…"):
    model = load_my_model()
    tokenizer = load_tokenizer()


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
    3: "😍",
    4: "😢",
    5: "😐"
}

label_class = {
    0: "marah",
    1: "takut",
    2: "senang",
    3: "cinta",
    4: "sedih",
    5: "netral"
}

max_length = 50

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from tensorflow.keras.preprocessing.sequence import pad_sequences


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
# PREDICT
# =========================
def predict_emotion(text):
    clean = preprocess(text)
    seq = tokenizer.texts_to_sequences([clean])
    pad = pad_sequences(seq, maxlen=max_length, padding='post')
    pred = model.predict(pad, verbose=0)[0]
    result = int(np.argmax(pred))
    return result, pred


def predict_batch(texts):
    cleaned = [preprocess(str(t)) for t in texts]
    seqs = tokenizer.texts_to_sequences(cleaned)
    pads = pad_sequences(seqs, maxlen=max_length, padding='post')
    preds = model.predict(pads, verbose=0)
    results = [int(np.argmax(p)) for p in preds]
    return results, preds


# =========================
# TOP BANNER
# =========================
st.markdown("""
<div class="top-banner">
    <div class="top-banner-icon">💬</div>
    <div>
        <p class="top-banner-title">Sistem Deteksi Emosi Pelanggan</p>
        <p class="top-banner-sub">Berbasis Deep Learning · Klasifikasi 6 Kelas Emosi</p>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# NAVIGATION
# =========================
if "menu" not in st.session_state:
    st.session_state.menu = "prediksi"

nav_items = [
    ("prediksi", "🔍 Prediksi Emosi"),
    ("batch", "📦 Analisis Batch"),
    ("evaluasi", "📊 Evaluasi Model"),
    ("dataset", "📁 Dataset"),
]

# Render invisible Streamlit buttons (hidden via CSS, triggered by HTML buttons via form hack)
# Better approach: use columns with styled markdown + real st.button hidden underneath
nav_cols = st.columns(4)
for col, (key, label) in zip(nav_cols, nav_items):
    is_active = st.session_state.menu == key
    with col:
        btn_style = """
            background-color: {bg} !important;
            color: {color} !important;
            border: 1px solid {border} !important;
            border-radius: 8px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: {weight} !important;
            font-size: 13px !important;
            padding: 9px 14px !important;
            width: 100% !important;
            cursor: pointer !important;
            transition: all 0.15s !important;
            box-shadow: {shadow} !important;
        """.format(
            bg="#1A56DB" if is_active else "#ffffff",
            color="#ffffff" if is_active else "#6B7280",
            border="#1A56DB" if is_active else "#E5E7EB",
            weight="600" if is_active else "500",
            shadow="0 1px 4px rgba(26,86,219,0.18)" if is_active else "none",
        )
        # Inject per-button style using unique key
        st.markdown(f"""
        <style>
        div[data-testid="column"]:has(button[kind="secondary"][data-testid="baseButton-secondary"]) {{}}
        [data-testid="stBaseButton-secondary"][aria-label="{label}"] {{
            {btn_style}
        }}
        </style>
        """, unsafe_allow_html=True)

        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.menu = key
            st.rerun()

menu = st.session_state.menu
st.markdown("<hr style='border:none;border-top:1px solid #E5E7EB;margin:4px 0 24px;'>", unsafe_allow_html=True)


# =========================
# 1. PREDIKSI
# =========================
if menu == "prediksi":

    st.markdown('<p class="section-heading">🔍 Prediksi Emosi Teks</p>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card"><p class="card-title">Masukkan Teks Ulasan</p>', unsafe_allow_html=True)
        user_input = st.text_area(
            label="Teks",
            placeholder="Ketik atau tempel teks ulasan pelanggan di sini…",
            height=150,
            label_visibility="collapsed"
        )
        analyze_btn = st.button("🔍 Analisis Emosi", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        if analyze_btn:
            if user_input.strip() == "":
                st.warning("⚠️ Teks belum diisi. Silakan masukkan teks terlebih dahulu.")
            else:
                result, pred = predict_emotion(user_input)
                cls = label_class[result]
                lbl = label_map[result]
                emj = label_emoji[result]

                # Emotion result card
                st.markdown(f"""
                <div class="emotion-result {cls}">
                    <div class="emotion-emoji">{emj}</div>
                    <div class="emotion-label {cls}">{lbl}</div>
                    <div style="font-size:12px;color:#9CA3AF;margin-top:4px;">Emosi terdeteksi</div>
                </div>
                """, unsafe_allow_html=True)

                # Probability bars
                st.markdown('<div class="card"><p class="card-title">Probabilitas Tiap Kelas</p>', unsafe_allow_html=True)
                for i in range(6):
                    pct = round(pred[i] * 100, 1)
                    width = round(pred[i] * 100)
                    st.markdown(f"""
                    <div class="prob-row">
                        <span class="prob-label">{label_emoji[i]} {label_map[i]}</span>
                        <div class="prob-bar-bg">
                            <div class="prob-bar-fill" style="width:{width}%;{'background:#1A56DB' if i==result else 'background:#9CA3AF'}"></div>
                        </div>
                        <span class="prob-pct">{pct}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div style="height:280px;display:flex;flex-direction:column;align-items:center;
                        justify-content:center;background:#F9FAFB;border-radius:12px;
                        border:1.5px dashed #D1D5DB;color:#9CA3AF;text-align:center;gap:8px;">
                <span style="font-size:32px">💬</span>
                <span style="font-size:14px;font-weight:500">Masukkan teks dan klik Analisis</span>
                <span style="font-size:12px">Hasil prediksi akan muncul di sini</span>
            </div>
            """, unsafe_allow_html=True)


# =========================
# 2. BATCH
# =========================
elif menu == "batch":

    st.markdown('<p class="section-heading">📦 Analisis Batch</p>', unsafe_allow_html=True)

    st.markdown('<div class="card"><p class="card-title">Upload File CSV</p>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;color:#6B7280;margin-bottom:12px;'>Pastikan kolom pertama berisi teks ulasan pelanggan.</p>", unsafe_allow_html=True)
    file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if file:
        df = pd.read_csv(file)
        st.markdown(f"<p style='font-size:13px;color:#374151;margin-bottom:12px;'><b>{len(df)}</b> baris data ditemukan.</p>", unsafe_allow_html=True)

        if st.button("▶ Proses Semua Data", use_container_width=False, type="primary"):
            with st.spinner("Memproses data…"):
                texts = df.iloc[:, 0].tolist()
                results, preds = predict_batch(texts)
                df["Emosi"] = [label_map[r] for r in results]
                df["Emoji"] = [label_emoji[r] for r in results]

            # Summary metrics
            counts = df["Emosi"].value_counts()
            st.markdown('<p class="section-heading" style="margin-top:24px;">Ringkasan Hasil</p>', unsafe_allow_html=True)

            metric_cols = st.columns(min(len(counts), 6))
            for col, (emosi, jumlah) in zip(metric_cols, counts.items()):
                emj = next(v for k, v in label_map.items() if v == emosi)
                emj_icon = next(v for k, v in label_emoji.items() if label_map[k] == emosi)
                with col:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size:22px">{emj_icon}</div>
                        <div class="metric-val">{jumlah}</div>
                        <div class="metric-lbl">{emosi}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Chart
            st.markdown("<div style='margin:28px 0 8px;'><b style='font-size:14px;color:#111827;'>Distribusi Emosi</b></div>", unsafe_allow_html=True)

            fig, ax = plt.subplots(figsize=(7, 3.2))
            colors = ["#EF4444","#F59E0B","#22C55E","#EC4899","#3B82F6","#9CA3AF"]
            bars = ax.barh(counts.index, counts.values,
                           color=colors[:len(counts)], height=0.55)
            for bar, val in zip(bars, counts.values):
                ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                        str(val), va='center', fontsize=11, color='#374151')
            ax.set_facecolor('#F9FAFB')
            fig.patch.set_facecolor('#F9FAFB')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E5E7EB')
            ax.spines['bottom'].set_color('#E5E7EB')
            ax.tick_params(colors='#6B7280', labelsize=11)
            ax.set_xlabel("Jumlah", fontsize=11, color='#6B7280')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            # Table
            st.markdown("<div style='margin:16px 0 8px;'><b style='font-size:14px;color:#111827;'>Detail Hasil</b></div>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, height=320)


# =========================
# 3. EVALUASI
# =========================
elif menu == "evaluasi":

    st.markdown('<p class="section-heading">📊 Evaluasi Model</p>', unsafe_allow_html=True)

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("72.6%", "Akurasi"),
        ("71.3%", "Presisi Rata-rata"),
        ("72.6%", "Recall Rata-rata"),
        ("71.8%", "F1-Score"),
    ]
    for col, (val, lbl) in zip([m1, m2, m3, m4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{val}</div>
                <div class="metric-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

    # Confusion Matrix
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Confusion Matrix</p>', unsafe_allow_html=True)

    cm = np.array([
        [47, 0, 11, 4, 0, 2],
        [0, 7, 0, 1, 0, 0],
        [2, 1, 207, 0, 0, 37],
        [0, 0, 3, 8, 1, 2],
        [4, 0, 2, 1, 7, 0],
        [3, 0, 46, 1, 0, 46]
    ])

    classes = list(label_map.values())

    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(cm, cmap="Blues")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax.set_xticks(range(6))
    ax.set_yticks(range(6))
    ax.set_xticklabels(classes, rotation=40, ha='right', fontsize=11, color='#374151')
    ax.set_yticklabels(classes, fontsize=11, color='#374151')
    ax.set_xlabel("Prediksi", fontsize=12, color='#6B7280', labelpad=8)
    ax.set_ylabel("Aktual", fontsize=12, color='#6B7280', labelpad=8)

    thresh = cm.max() / 2.0
    for i in range(6):
        for j in range(6):
            ax.text(j, i, cm[i, j], ha='center', va='center',
                    fontsize=11, fontweight='600',
                    color='white' if cm[i, j] > thresh else '#1F2937')

    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.spines[:].set_color('#E5E7EB')
    ax.tick_params(colors='#374151')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown('</div>', unsafe_allow_html=True)

    # Per-class report
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="card-title">Laporan Per Kelas</p>', unsafe_allow_html=True)

    report_data = {
        "Emosi":     ["Marah 😠", "Takut 😨", "Senang 😊", "Cinta ❤️", "Sedih 😢", "Netral 😐"],
        "Presisi":   ["74.6%", "87.5%", "76.2%", "53.3%", "87.5%", "51.7%"],
        "Recall":    ["73.4%", "87.5%", "83.5%", "57.1%", "50.0%", "47.9%"],
        "F1-Score":  ["74.0%", "87.5%", "79.7%", "55.2%", "63.6%", "49.7%"],
    }
    st.dataframe(pd.DataFrame(report_data), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 4. DATASET
# =========================
elif menu == "dataset":

    st.markdown('<p class="section-heading">📁 Dataset</p>', unsafe_allow_html=True)

    st.markdown('<div class="card"><p class="card-title">Upload Dataset CSV</p>', unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;color:#6B7280;margin-bottom:12px;'>Upload file CSV untuk melihat dan mengeksplorasi isi dataset.</p>", unsafe_allow_html=True)
    file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if file:
        df = pd.read_csv(file)

        total = len(df)
        cols_count = len(df.columns)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{total:,}</div><div class="metric-lbl">Total Baris</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-box"><div class="metric-val">{cols_count}</div><div class="metric-lbl">Kolom</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><p class="card-title">Pratinjau Data</p>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=380)
        st.markdown('</div>', unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.markdown("""
<div style="text-align:center;padding:28px 0 12px;color:#9CA3AF;font-size:12px;">
    Sistem Deteksi Emosi Pelanggan &nbsp;·&nbsp; Skripsi 2025 &nbsp;·&nbsp; Deep Learning NLP
</div>
""", unsafe_allow_html=True)
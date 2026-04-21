import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Sistem Deteksi Emosi",
    page_icon="🧠",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #F8F9FB;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ── Header ── */
    .main-header {
        background: #ffffff;
        border-bottom: 1px solid #E5E7EB;
        padding: 18px 0 14px;
        margin-bottom: 32px;
        text-align: center;
    }
    .main-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
        letter-spacing: -0.4px;
        margin: 0;
    }
    .main-title span {
        color: #2563EB;
    }
    .main-subtitle {
        font-size: 12.5px;
        color: #9CA3AF;
        margin: 4px 0 0;
        font-weight: 400;
    }

    /* ── Navigation ── */
    .nav-container {
        display: flex;
        gap: 6px;
        background: #ffffff;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 5px;
        margin-bottom: 32px;
    }

    /* ── Card ── */
    .card {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #E9EBF0;
        padding: 22px 24px;
        margin-bottom: 18px;
    }
    .card-title {
        font-size: 14px;
        font-weight: 600;
        color: #111827;
        margin: 0 0 14px;
    }

    /* ── Section heading ── */
    .section-heading {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
        margin: 0 0 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #E5E7EB;
    }

    /* ── Sub-tab pills ── */
    .subtab-wrap {
        display: flex;
        gap: 8px;
        margin-bottom: 24px;
    }
    .subtab-pill {
        padding: 7px 18px;
        border-radius: 99px;
        font-size: 13px;
        font-weight: 500;
        border: 1.5px solid #E5E7EB;
        background: #ffffff;
        color: #6B7280;
    }
    .subtab-pill.active {
        background: #EFF6FF;
        color: #2563EB;
        border-color: #BFDBFE;
        font-weight: 600;
    }

    /* ── Emotion result ── */
    .emotion-result {
        border-radius: 12px;
        padding: 22px 24px;
        text-align: center;
        margin-bottom: 16px;
    }
    .emotion-result.marah  { background: #FEF2F2; border: 1px solid #FECACA; }
    .emotion-result.takut  { background: #FFFBEB; border: 1px solid #FDE68A; }
    .emotion-result.senang { background: #F0FDF4; border: 1px solid #BBF7D0; }
    .emotion-result.cinta  { background: #FDF2F8; border: 1px solid #FBCFE8; }
    .emotion-result.sedih  { background: #EFF6FF; border: 1px solid #BFDBFE; }
    .emotion-result.netral { background: #F9FAFB; border: 1px solid #E5E7EB; }

    .emotion-emoji { font-size: 40px; margin-bottom: 6px; }
    .emotion-label { font-size: 20px; font-weight: 700; letter-spacing: -0.3px; }
    .emotion-label.marah  { color: #DC2626; }
    .emotion-label.takut  { color: #D97706; }
    .emotion-label.senang { color: #16A34A; }
    .emotion-label.cinta  { color: #DB2777; }
    .emotion-label.sedih  { color: #2563EB; }
    .emotion-label.netral { color: #6B7280; }

    /* ── Probability bar ── */
    .prob-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
    .prob-label { font-size: 13px; color: #374151; width: 80px; }
    .prob-bar-bg { flex: 1; background: #F3F4F6; border-radius: 99px; height: 7px; overflow: hidden; }
    .prob-bar-fill { height: 100%; border-radius: 99px; }
    .prob-pct { font-size: 12px; color: #6B7280; width: 40px; text-align: right; font-weight: 500; }

    /* ── Metric box ── */
    .metric-box {
        background: #F0F5FF;
        border-radius: 10px;
        padding: 18px 16px;
        text-align: center;
        border: 1px solid #C7D7FF;
    }
    .metric-val { font-size: 26px; font-weight: 700; color: #2563EB; }
    .metric-lbl { font-size: 11.5px; color: #6B7280; margin-top: 4px; }

    /* ── Dataset info badge ── */
    .info-badge {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        color: #1D4ED8;
        margin-bottom: 16px;
    }
    .info-badge b { font-weight: 600; }

    /* ── Streamlit overrides ── */
    .stTextArea textarea {
        border-radius: 10px !important;
        border-color: #D1D5DB !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
    }
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #2563EB !important;
        color: #ffffff !important;
        border: 1px solid #2563EB !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        box-shadow: 0 1px 4px rgba(37,99,235,0.20) !important;
    }
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #1D4ED8 !important;
    }
    .stButton > button[data-testid="baseButton-secondary"] {
        background-color: #ffffff !important;
        color: #6B7280 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #F3F4F6 !important;
        color: #374151 !important;
    }
    div[data-testid="stAlert"] { border-radius: 10px !important; }
    .stProgress > div > div { background-color: #2563EB !important; }

    /* ── Divider ── */
    .divider { border: none; border-top: 1px solid #E5E7EB; margin: 4px 0 28px; }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        padding: 28px 0 12px;
        color: #9CA3AF;
        font-size: 12px;
        border-top: 1px solid #E5E7EB;
        margin-top: 40px;
    }
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
# LABELS
# =========================
label_map = {0: "Marah", 1: "Takut", 2: "Senang", 3: "Cinta", 4: "Sedih", 5: "Netral"}
label_emoji = {0: "😠", 1: "😨", 2: "😊", 3: "😍", 4: "😢", 5: "😐"}
label_class = {0: "marah", 1: "takut", 2: "senang", 3: "cinta", 4: "sedih", 5: "netral"}
label_color = {0: "#EF4444", 1: "#F59E0B", 2: "#22C55E", 3: "#EC4899", 4: "#3B82F6", 5: "#9CA3AF"}

max_length = 50

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from tensorflow.keras.preprocessing.sequence import pad_sequences


# =========================
# HELPERS
# =========================
def preprocess(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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
# HEADER
# =========================
st.markdown("""
<div class="main-header">
    <p class="main-title">🧠 <span>Sistem Deteksi Emosi</span></p>
    <p class="main-subtitle">Deep Learning · Klasifikasi 6 Kelas Emosi · Skripsi 2025</p>
</div>
""", unsafe_allow_html=True)


# =========================
# NAVIGATION (3 MENU)
# =========================
if "menu" not in st.session_state:
    st.session_state.menu = "prediksi"
if "sub_prediksi" not in st.session_state:
    st.session_state.sub_prediksi = "kalimat"

nav_items = [
    ("prediksi",  "🔍 Prediksi Emosi"),
    ("evaluasi",  "📊 Evaluasi Model"),
    ("dataset",   "📁 Dataset"),
]

nav_cols = st.columns(3)
for col, (key, label) in zip(nav_cols, nav_items):
    is_active = st.session_state.menu == key
    with col:
        if st.button(label, key=f"nav_{key}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.menu = key
            st.rerun()

st.markdown("<hr class='divider'>", unsafe_allow_html=True)
menu = st.session_state.menu


# ══════════════════════════════════════
#  MENU 1 — PREDIKSI EMOSI
# ══════════════════════════════════════
if menu == "prediksi":

    st.markdown('<p class="section-heading">🔍 Prediksi Emosi</p>', unsafe_allow_html=True)

    # Sub-tab: Kalimat / Batch
    sub_cols = st.columns([1, 1, 4])
    with sub_cols[0]:
        if st.button("✏️ Per Kalimat",
                     key="sub_kalimat",
                     use_container_width=True,
                     type="primary" if st.session_state.sub_prediksi == "kalimat" else "secondary"):
            st.session_state.sub_prediksi = "kalimat"
            st.rerun()
    with sub_cols[1]:
        if st.button("📦 Batch CSV",
                     key="sub_batch",
                     use_container_width=True,
                     type="primary" if st.session_state.sub_prediksi == "batch" else "secondary"):
            st.session_state.sub_prediksi = "batch"
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Sub: Per Kalimat ──
    if st.session_state.sub_prediksi == "kalimat":

        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown('<div class="card"><p class="card-title">Masukkan Teks Ulasan</p>', unsafe_allow_html=True)
            user_input = st.text_area(
                label="Teks",
                placeholder="Ketik atau tempel teks ulasan pelanggan di sini…",
                height=160,
                label_visibility="collapsed"
            )
            analyze_btn = st.button("🔍 Analisis Emosi", use_container_width=True, type="primary")
            st.markdown("""
            <p style="font-size:12px;color:#9CA3AF;margin-top:8px;">
                Masukkan satu kalimat atau paragraf, lalu klik Analisis Emosi untuk mendapatkan prediksi.
            </p>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            if analyze_btn:
                if user_input.strip() == "":
                    st.warning("⚠️ Teks belum diisi. Silakan masukkan teks terlebih dahulu.")
                else:
                    result, pred = predict_emotion(user_input)
                    cls   = label_class[result]
                    lbl   = label_map[result]
                    emj   = label_emoji[result]

                    st.markdown(f"""
                    <div class="emotion-result {cls}">
                        <div class="emotion-emoji">{emj}</div>
                        <div class="emotion-label {cls}">{lbl}</div>
                        <div style="font-size:12px;color:#9CA3AF;margin-top:4px;">Emosi terdeteksi</div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<div class="card"><p class="card-title">Probabilitas Tiap Kelas</p>', unsafe_allow_html=True)
                    for i in range(6):
                        pct   = round(pred[i] * 100, 1)
                        width = round(pred[i] * 100)
                        fill_color = label_color[i] if i == result else "#D1D5DB"
                        st.markdown(f"""
                        <div class="prob-row">
                            <span class="prob-label">{label_emoji[i]} {label_map[i]}</span>
                            <div class="prob-bar-bg">
                                <div class="prob-bar-fill" style="width:{width}%;background:{fill_color};"></div>
                            </div>
                            <span class="prob-pct">{pct}%</span>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="height:260px;display:flex;flex-direction:column;align-items:center;
                            justify-content:center;background:#F9FAFB;border-radius:12px;
                            border:1.5px dashed #D1D5DB;color:#9CA3AF;text-align:center;gap:8px;">
                    <span style="font-size:32px">💬</span>
                    <span style="font-size:14px;font-weight:500">Hasil prediksi akan muncul di sini</span>
                    <span style="font-size:12px">Masukkan teks dan klik Analisis Emosi</span>
                </div>
                """, unsafe_allow_html=True)

    # ── Sub: Batch CSV ──
    else:

        st.markdown('<div class="card"><p class="card-title">Upload File CSV</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-badge">
            <b>Format yang diperlukan:</b> File CSV dengan kolom pertama berisi teks ulasan pelanggan.
            Sistem akan memproses setiap baris secara otomatis dan menampilkan hasil beserta distribusi emosi.
        </div>
        """, unsafe_allow_html=True)
        file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        if file:
            df = pd.read_csv(file)
            st.markdown(f"<p style='font-size:13px;color:#374151;margin-bottom:16px;'><b>{len(df)}</b> baris data ditemukan dalam file.</p>", unsafe_allow_html=True)

            if st.button("▶ Proses Semua Data", use_container_width=False, type="primary"):
                with st.spinner("Memproses data…"):
                    texts = df.iloc[:, 0].tolist()
                    results, preds = predict_batch(texts)
                    df["Emosi"] = [label_map[r] for r in results]
                    df["Emoji"] = [label_emoji[r] for r in results]

                counts = df["Emosi"].value_counts()
                st.markdown('<p class="section-heading" style="margin-top:24px;">Ringkasan Hasil</p>', unsafe_allow_html=True)

                metric_cols = st.columns(min(len(counts), 6))
                for col, (emosi, jumlah) in zip(metric_cols, counts.items()):
                    emj_icon = next(v for k, v in label_emoji.items() if label_map[k] == emosi)
                    with col:
                        st.markdown(f"""
                        <div class="metric-box">
                            <div style="font-size:22px">{emj_icon}</div>
                            <div class="metric-val">{jumlah}</div>
                            <div class="metric-lbl">{emosi}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<div style='margin:28px 0 8px;'><b style='font-size:14px;color:#111827;'>Distribusi Emosi</b></div>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(7, 3.2))
                colors = ["#EF4444","#F59E0B","#22C55E","#EC4899","#3B82F6","#9CA3AF"]
                bars = ax.barh(counts.index, counts.values, color=colors[:len(counts)], height=0.55)
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

                st.markdown("<div style='margin:16px 0 8px;'><b style='font-size:14px;color:#111827;'>Detail Hasil</b></div>", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, height=320)

                csv_out = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="⬇️ Unduh Hasil sebagai CSV",
                    data=csv_out,
                    file_name="hasil_prediksi_emosi.csv",
                    mime="text/csv"
                )


# ══════════════════════════════════════
#  MENU 2 — EVALUASI MODEL
# ══════════════════════════════════════
elif menu == "evaluasi":

    st.markdown('<p class="section-heading">📊 Evaluasi Model</p>', unsafe_allow_html=True)

    # Metric cards
    metrics = [
        ("72.6%", "Akurasi"),
        ("71.3%", "Presisi Rata-rata"),
        ("72.6%", "Recall Rata-rata"),
        ("71.8%", "F1-Score"),
    ]
    m_cols = st.columns(4)
    for col, (val, lbl) in zip(m_cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{val}</div>
                <div class="metric-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1.1, 1], gap="large")

    # Confusion Matrix
    with col_a:
        st.markdown('<div class="card"><p class="card-title">Confusion Matrix</p>', unsafe_allow_html=True)

        cm = np.array([
            [47,  0, 11,  4,  0,  2],
            [ 0,  7,  0,  1,  0,  0],
            [ 2,  1,207,  0,  0, 37],
            [ 0,  0,  3,  8,  1,  2],
            [ 4,  0,  2,  1,  7,  0],
            [ 3,  0, 46,  1,  0, 46]
        ])
        classes = list(label_map.values())

        fig, ax = plt.subplots(figsize=(6.5, 5))
        im = ax.imshow(cm, cmap="Blues")
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_xticks(range(6)); ax.set_yticks(range(6))
        ax.set_xticklabels(classes, rotation=40, ha='right', fontsize=10.5, color='#374151')
        ax.set_yticklabels(classes, fontsize=10.5, color='#374151')
        ax.set_xlabel("Prediksi", fontsize=11, color='#6B7280', labelpad=8)
        ax.set_ylabel("Aktual",   fontsize=11, color='#6B7280', labelpad=8)
        thresh = cm.max() / 2.0
        for i in range(6):
            for j in range(6):
                ax.text(j, i, cm[i, j], ha='center', va='center',
                        fontsize=10.5, fontweight='600',
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
    with col_b:
        st.markdown('<div class="card"><p class="card-title">Laporan Per Kelas</p>', unsafe_allow_html=True)
        report_data = {
            "Emosi":   ["Marah 😠","Takut 😨","Senang 😊","Cinta ❤️","Sedih 😢","Netral 😐"],
            "Presisi": ["74.6%","87.5%","76.2%","53.3%","87.5%","51.7%"],
            "Recall":  ["73.4%","87.5%","83.5%","57.1%","50.0%","47.9%"],
            "F1-Score":["74.0%","87.5%","79.7%","55.2%","63.6%","49.7%"],
        }
        st.dataframe(pd.DataFrame(report_data), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Penjelasan metrik
        st.markdown("""
        <div class="card">
            <p class="card-title">Keterangan Metrik</p>
            <table style="width:100%;font-size:12.5px;color:#374151;border-collapse:collapse;">
                <tr style="background:#F3F4F6;">
                    <td style="padding:7px 10px;font-weight:600;border-radius:6px;">Akurasi</td>
                    <td style="padding:7px 10px;">Persentase prediksi yang benar dari seluruh data uji.</td>
                </tr>
                <tr>
                    <td style="padding:7px 10px;font-weight:600;">Presisi</td>
                    <td style="padding:7px 10px;">Dari semua prediksi suatu kelas, berapa yang benar.</td>
                </tr>
                <tr style="background:#F3F4F6;">
                    <td style="padding:7px 10px;font-weight:600;border-radius:6px;">Recall</td>
                    <td style="padding:7px 10px;">Dari semua data kelas tersebut, berapa yang terdeteksi.</td>
                </tr>
                <tr>
                    <td style="padding:7px 10px;font-weight:600;">F1-Score</td>
                    <td style="padding:7px 10px;">Rata-rata harmonis Presisi dan Recall.</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════
#  MENU 3 — DATASET
# ══════════════════════════════════════
elif menu == "dataset":

    st.markdown('<p class="section-heading">📁 Dataset</p>', unsafe_allow_html=True)

    # Penjelasan fungsi halaman
    st.markdown("""
    <div class="info-badge" style="background:#F0FDF4;border-color:#BBF7D0;color:#15803D;">
        <b>Fungsi Halaman Ini:</b> Halaman ini digunakan untuk mengunggah dan mengeksplorasi dataset latih/uji
        yang digunakan dalam penelitian. Anda dapat melihat distribusi label emosi, statistik dataset,
        serta pratinjau data sebelum digunakan untuk pelatihan model.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><p class="card-title">Upload File Dataset (CSV)</p>', unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:13px;color:#6B7280;margin-bottom:12px;'>
        Upload file CSV dataset. Pastikan terdapat kolom <b>teks</b> (teks ulasan) dan kolom <b>label</b> (kelas emosi).
        Sistem akan menampilkan statistik, distribusi label, dan pratinjau data secara otomatis.
    </p>
    """, unsafe_allow_html=True)
    file_ds = st.file_uploader("Upload CSV Dataset", type=["csv"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if file_ds:
        df_ds = pd.read_csv(file_ds)

        # ── Statistik Umum ──
        total     = len(df_ds)
        n_cols    = len(df_ds.columns)
        n_missing = int(df_ds.isnull().sum().sum())
        n_dup     = int(df_ds.duplicated().sum())

        st.markdown('<p style="font-size:14px;font-weight:600;color:#111827;margin-bottom:12px;">Statistik Dataset</p>', unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        stats = [
            (f"{total:,}", "Total Data"),
            (f"{n_cols}", "Jumlah Kolom"),
            (f"{n_missing}", "Nilai Kosong"),
            (f"{n_dup}", "Data Duplikat"),
        ]
        for col, (val, lbl) in zip([s1, s2, s3, s4], stats):
            with col:
                st.markdown(f'<div class="metric-box"><div class="metric-val">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

        # ── Distribusi Label (jika ada kolom label) ──
        label_col = None
        for col_name in df_ds.columns:
            if col_name.lower() in ["label", "emosi", "emotion", "kategori", "class"]:
                label_col = col_name
                break

        if label_col:
            st.markdown(f'<p style="font-size:14px;font-weight:600;color:#111827;margin:4px 0 12px;">Distribusi Label <span style="font-size:12px;color:#6B7280;font-weight:400;">(kolom: <i>{label_col}</i>)</span></p>', unsafe_allow_html=True)

            dist = df_ds[label_col].value_counts()

            d_cols = st.columns(min(len(dist), 6))
            for col, (lbl_val, cnt) in zip(d_cols, dist.items()):
                # cari emoji jika label cocok
                emj_icon = next((v for k, v in label_map.items() if label_map[k].lower() == str(lbl_val).lower()), "🏷️")
                with col:
                    pct = round(cnt / total * 100, 1)
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size:20px">{emj_icon}</div>
                        <div class="metric-val" style="font-size:20px;">{cnt}</div>
                        <div class="metric-lbl">{lbl_val} ({pct}%)</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

            # Bar chart distribusi
            fig2, ax2 = plt.subplots(figsize=(7, 3))
            colors2 = ["#EF4444","#F59E0B","#22C55E","#EC4899","#3B82F6","#9CA3AF"]
            bars2 = ax2.bar(dist.index.astype(str), dist.values,
                            color=colors2[:len(dist)], width=0.5)
            for bar, val in zip(bars2, dist.values):
                ax2.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                         str(val), ha='center', fontsize=11, color='#374151')
            ax2.set_facecolor('#F9FAFB')
            fig2.patch.set_facecolor('#F9FAFB')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['left'].set_color('#E5E7EB')
            ax2.spines['bottom'].set_color('#E5E7EB')
            ax2.tick_params(colors='#6B7280', labelsize=11)
            ax2.set_ylabel("Jumlah Data", fontsize=11, color='#6B7280')
            ax2.set_xlabel("Kelas Emosi", fontsize=11, color='#6B7280')
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()
        else:
            st.info("ℹ️ Kolom label tidak ditemukan secara otomatis. Distribusi label tidak ditampilkan.")

        # ── Pratinjau Data ──
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="card"><p class="card-title">Pratinjau Data</p>', unsafe_allow_html=True)

        n_preview = st.slider("Jumlah baris yang ditampilkan", min_value=5, max_value=min(200, total), value=20, step=5)
        st.dataframe(df_ds.head(n_preview), use_container_width=True, height=340)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Download dataset yang sudah difilter ──
        st.download_button(
            label="⬇️ Unduh Dataset (CSV)",
            data=df_ds.to_csv(index=False).encode("utf-8"),
            file_name="dataset_emosi.csv",
            mime="text/csv"
        )

    else:
        st.markdown("""
        <div style="height:220px;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;background:#F9FAFB;border-radius:12px;
                    border:1.5px dashed #D1D5DB;color:#9CA3AF;text-align:center;gap:8px;">
            <span style="font-size:32px">📂</span>
            <span style="font-size:14px;font-weight:500">Belum ada dataset yang diunggah</span>
            <span style="font-size:12px">Upload file CSV untuk mulai eksplorasi data</span>
        </div>
        """, unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.markdown("""
<div class="app-footer">
    Sistem Deteksi Emosi &nbsp;·&nbsp; Skripsi 2025 &nbsp;·&nbsp; Deep Learning NLP
</div>
""", unsafe_allow_html=True)
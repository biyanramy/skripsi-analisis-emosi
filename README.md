# 💬 Sistem Deteksi Emosi Pelanggan Berbasis Bi-LSTM

## 📌 Deskripsi

Proyek ini merupakan implementasi **Natural Language Processing (NLP)** untuk mendeteksi emosi pelanggan berdasarkan teks ulasan menggunakan metode **Bidirectional Long Short-Term Memory (Bi-LSTM)**.

Sistem mampu mengklasifikasikan emosi ke dalam 6 kategori:

* 😠 Marah
* 😨 Takut
* 😊 Senang
* ❤️ Cinta
* 😢 Sedih
* 😐 Netral

Aplikasi dibuat menggunakan **Streamlit** sebagai antarmuka interaktif.

---

## 🧠 Metodologi

Tahapan yang dilakukan dalam penelitian ini:

1. **Preprocessing**

   * Case folding
   * Cleaning text
   * Tokenizing
   * Stopword removal

2. **Feature Extraction**

   * Word Embedding menggunakan **FastText**

3. **Model**

   * Deep Learning: **Bidirectional LSTM (Bi-LSTM)**

4. **Evaluasi**

   * Accuracy
   * Precision
   * Recall
   * F1-Score
   * Confusion Matrix

---

## 📂 Struktur Project

```bash
skripsi-analisis-emosi/
│
├── app.py
├── preprocessing.py
├── tokenizing.py
├── bilstm.py
│
├── tokenizer.pkl
├── embedding_matrix.npy
│
├── accuracy.png
├── loss.png
├── confusion_matrix.png
│
├── requirements.txt
└── README.md
```

---

## ☁️ Download File Penting

Karena keterbatasan GitHub, file besar tidak disertakan dalam repository.

Silakan download melalui link berikut:

* 📦 Dataset
  (https://drive.google.com/drive/folders/1E7W87MnqBjYx6Pg-thOkT-FC9RBqzirc?usp=sharing)

* 🤖 Model Bi-LSTM
  (https://drive.google.com/file/d/1g5IDYSPlfOCIP1gTl5gVsR1wYZqi4W7i/view?usp=sharing)
  
* 🔤 FastText Model
  (https://drive.google.com/file/d/1IMSG4bBiWOz1QlNkF8oPU_NtHrjNE6Yl/view?usp=sharing)

---

## ⚙️ Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/biyanramy/skripsi-analisis-emosi.git
cd skripsi-analisis-emosi
```

---

### 2. Buat Virtual Environment (Python 3.10)

```bash
python3.10 -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

### 3. Install Dependency

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Download File dari Google Drive

Letakkan file berikut di dalam folder project:

* `model_emotion.keras`
* `fasttext_model.bin`
* dataset `.csv`

---

### 5. Jalankan Aplikasi

```bash
python -m streamlit run app.py
```

---

## 📊 Fitur Aplikasi

* 🔍 Prediksi emosi dari teks
* 📦 Analisis batch (upload CSV)
* 📊 Evaluasi model (confusion matrix & metrik)
* 📁 Eksplorasi dataset

---

## 🎯 Tujuan Penelitian

Penelitian ini bertujuan untuk:

* Mengklasifikasikan emosi pelanggan secara otomatis
* Membantu analisis sentimen produk/layanan
* Mengimplementasikan model deep learning pada teks Bahasa Indonesia

---

## 👨‍💻 Author

**Abyan Ramy A**
Mahasiswa Informatika

---

## 📌 Teknologi yang Digunakan

* Python
* TensorFlow / Keras
* Streamlit
* Scikit-learn
* FastText

---

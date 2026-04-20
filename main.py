# ==============================
# 1. IMPORT LIBRARY
# ==============================
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense


# ==============================
# 2. LOAD DATA
# ==============================
df = pd.read_csv("dataset_osb.csv", sep=None, engine='python')

# ambil kolom ulasan saja
df = df[["Ulasan"]]
df = df.rename(columns={"Ulasan": "text"})

# hapus data kosong
df = df.dropna(subset=["text"])


# ==============================
# 3. CLEANING TEXT
# ==============================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\b\d+\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text"].apply(clean_text)


# ==============================
# 4. AUTO LABEL (LEXICON)
# ==============================
positive_words = ["bagus","mantap","cepat","puas","rekomendasi","suka","aman"]
negative_words = ["jelek","lama","rusak","kecewa","buruk","parah"]

def label_text(text):
    pos = sum(word in text for word in positive_words)
    neg = sum(word in text for word in negative_words)

    if pos > neg:
        return "senang"
    elif neg > pos:
        return "marah"
    else:
        return "netral"

df["label"] = df["clean_text"].apply(label_text)


# ==============================
# 5. CEK DISTRIBUSI LABEL
# ==============================
print("\nDistribusi Label:")
print(df["label"].value_counts())


# ==============================
# 6. TOKENIZING
# ==============================
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df["clean_text"])

X = tokenizer.texts_to_sequences(df["clean_text"])
X = pad_sequences(X, maxlen=50)


# ==============================
# 7. ENCODE LABEL
# ==============================
le = LabelEncoder()
y = le.fit_transform(df["label"])


# ==============================
# 8. SPLIT DATA
# ==============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ==============================
# 9. MODEL BI-LSTM
# ==============================
model = Sequential()
model.add(Embedding(input_dim=5000, output_dim=128, input_length=50))
model.add(Bidirectional(LSTM(64)))
model.add(Dense(3, activation='softmax'))

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

model.summary()


# ==============================
# 10. TRAINING
# ==============================
model.fit(X_train, y_train, epochs=5, batch_size=32)


# ==============================
# 11. EVALUASI
# ==============================
y_pred = model.predict(X_test)
y_pred = y_pred.argmax(axis=1)

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))


# ==============================
# 12. SAVE MODEL (OPSIONAL)
# ==============================
model.save("model_bilstm.h5")
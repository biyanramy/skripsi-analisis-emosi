import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# ambil data
df = pd.read_csv("dataset_labeled_done.csv")

# bersihkan
df["clean_text"] = df["clean_text"].fillna("").astype(str)
df = df[df["label"].notna()]  # hapus label kosong

# shuffle data
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

texts = df["clean_text"]
labels = df["label_final"].astype(int)

# tokenizer
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)

# simpan tokenizer
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("✅ tokenizer disimpan")

# sequences
sequences = tokenizer.texts_to_sequences(texts)

# padding
max_length = 50
X = pad_sequences(sequences, maxlen=max_length, padding='post')
y = labels.values

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# simpan
np.save("X_train.npy", X_train)
np.save("X_test.npy", X_test)
np.save("y_train.npy", y_train)
np.save("y_test.npy", y_test)

print("✅ Tokenizing selesai")
print("Shape X_train:", X_train.shape)
print("Shape X_test:", X_test.shape)
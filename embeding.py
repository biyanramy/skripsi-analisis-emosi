import pandas as pd
import numpy as np
import fasttext
import pickle

# load data
df = pd.read_csv("dataset_labeled_done.csv")
df["clean_text"] = df["clean_text"].fillna("").astype(str)

texts = df["clean_text"].tolist()
print("Jumlah data:", len(texts))

# load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

word_index = tokenizer.word_index
print("Jumlah vocab:", len(word_index))

# simpan ke file
with open("sentences.txt", "w") as f:
    for text in texts:
        if text.strip() != "":
            f.write(text + "\n")

print("✅ sentences.txt siap")

# train fasttext
ft_model = fasttext.train_unsupervised(
    "sentences.txt",
    model='skipgram',
    dim=100,
    epoch=20,
    minn=2,
    maxn=5
)

ft_model.save_model("fasttext_model.bin")
print("✅ FastText selesai")

# embedding matrix
embedding_dim = 100
max_words = 5000

embedding_matrix = np.zeros((max_words, embedding_dim))

covered = 0

for word, i in word_index.items():
    if i < max_words:
        vector = ft_model.get_word_vector(word)
        if vector is not None:
            embedding_matrix[i] = vector
            covered += 1

np.save("embedding_matrix.npy", embedding_matrix)

print("✅ Embedding berhasil dibuat")
print("Shape:", embedding_matrix.shape)
print(f"Coverage: {covered}/{max_words}")
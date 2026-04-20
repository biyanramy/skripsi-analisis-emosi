import pandas as pd
import re

# =========================
# SLANG + TYPO FIX
# =========================
slang_dict = {
    "gk": "tidak",
    "ga": "tidak",
    "bgt": "banget",
    "parahh": "parah",
    "jelekkkk": "jelek",
    "mantapp": "mantap",
    "lngs": "langsung",
    "dtng": "datang",
    "smpe": "sampai",
    "kmrn": "kemarin",
    "ajar": "belajar",
    "sklh": "sekolah",
    "rmh": "rumah",
    "psn": "pesan",
    "sy": "saya",
    "yg": "yang",
    "bhs": "bahasa",
    "aq": "aku",
    "k": "ke",
    "utk": "untuk",
    "sdh": "sudah",
    "bngt": "banget",
    "dgn": "dengan"
}

def remove_noise(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

def normalize_slang(text):
    words = text.split()
    words = [slang_dict.get(word, word) for word in words]
    return " ".join(words)

def remove_repeated_chars(text):
    return re.sub(r'(.)\1+', r'\1', text)

def preprocess(text):
    text = str(text).lower()
    text = remove_noise(text)
    text = remove_repeated_chars(text)
    text = normalize_slang(text)
    return text

if __name__ == "__main__":
    df = pd.read_csv("dataset_osb.csv")

    df.rename(columns={
        "Username": "username",
        "Ulasan": "ulasan"
    }, inplace=True)

    df["clean_text"] = df["ulasan"].apply(preprocess)

    # Ambil 3 kolom
    df_final = df[["username", "ulasan", "clean_text"]]

    # Tambah kolom label kosong
    df_final["label"] = ""

    # Simpan
    df_final.to_csv("dataset_clean.csv", index=False)

    print("Preprocessing selesai!")
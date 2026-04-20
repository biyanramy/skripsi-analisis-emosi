import pandas as pd

df = pd.read_csv("dataset_labeled.csv")

df["clean_text"] = df["clean_text"].fillna("").astype(str)

emotion_map = {
    0.0: "Marah 😠",
    1.0: "Takut 😨",
    2.0: "Senang 😊",
    3.0: "Cinta ❤️",
    4.0: "Sedih 😢",
    5.0: "Netral 😐"
}

labels = []

for i, text in enumerate(df["clean_text"]):
    print("\n========================")
    print(f"Data ke-{i+1}")
    print("Text :", text)

    if text.strip() == "":
        print("⚠️ Data kosong, skip otomatis")
        labels.append(None)
        continue

    # ambil label dari AI
    pred = df.loc[i, "label"]  # ⬅️ penting

    print(f"Label AI: {emotion_map.get(pred, 'Unknown')} ({pred})")

    # validasi user
    user_input = input("Revisi? (Enter=benar, 0-5=ganti, s=skip): ")

    if user_input == "":
        labels.append(pred)
    elif user_input in ["0","1","2","3","4","5"]:
        labels.append(float(user_input))
    elif user_input.lower() == "s":
        labels.append(None)
    else:
        labels.append(pred)

# simpan hasil final
df["label_final"] = labels

df = df[df["label_final"].notna()]

df.to_csv("dataset_labeled_done.csv", index=False)

print("Validasi selesai!")
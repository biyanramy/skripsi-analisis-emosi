import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam

np.random.seed(42)

# =========================
# LOAD DATA
# =========================
X_train = np.load("X_train.npy")
X_test = np.load("X_test.npy")
y_train = np.load("y_train.npy")
y_test = np.load("y_test.npy")

embedding_matrix = np.load("embedding_matrix.npy")

# =========================
# CLASS WEIGHT
# =========================
classes = np.unique(y_train)

weights = compute_class_weight(
    class_weight='balanced',
    classes=classes,
    y=y_train
)

class_weights = dict(zip(classes, weights))
print("Class Weights:", class_weights)

vocab_size = embedding_matrix.shape[0]
embedding_dim = embedding_matrix.shape[1]
max_length = X_train.shape[1]

# =========================
# MODEL (IMPROVED 🔥)
# =========================
model = Sequential([
    Embedding(
        input_dim=vocab_size,
        output_dim=embedding_dim,
        weights=[embedding_matrix],
        input_length=max_length,
        trainable=True   # 🔥 penting
    ),

    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.3),

    Bidirectional(LSTM(64)),
    Dropout(0.3),

    Dense(64, activation='relu'),
    Dropout(0.2),

    Dense(6, activation='softmax')
])

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=Adam(learning_rate=0.0003),  # 🔥 lebih stabil
    metrics=['accuracy']
)

model.summary()

# =========================
# EARLY STOPPING
# =========================
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# =========================
# TRAINING
# =========================
history = model.fit(
    X_train, y_train,
    epochs=20,  # 🔥 ditambah
    batch_size=32,
    validation_split=0.2,
    class_weight=class_weights,
    callbacks=[early_stop]
)

# =========================
# EVALUASI
# =========================
loss, acc = model.evaluate(X_test, y_test)
print("\nTest Accuracy:", acc)

# =========================
# PREDIKSI
# =========================
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

print("\nDistribusi prediksi:")
print(np.bincount(y_pred_classes, minlength=6))

# =========================
# METRICS
# =========================
labels = [0,1,2,3,4,5]
target_names = ["marah", "takut", "senang", "cinta", "sedih", "netral"]

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred_classes,
    labels=labels,
    target_names=target_names,
    zero_division=0   # 🔥 hilangkan warning
))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred_classes, labels=labels)
print(cm)

# =========================
# VISUAL CONFUSION MATRIX
# =========================
plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar()

plt.xticks(range(6), target_names, rotation=45)
plt.yticks(range(6), target_names)

for i in range(6):
    for j in range(6):
        plt.text(j, i, cm[i, j], ha='center', va='center')

plt.tight_layout()
plt.show()

# =========================
# GRAFIK
# =========================
plt.figure()
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.legend()
plt.title("Accuracy")
plt.show()

plt.figure()
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.legend()
plt.title("Loss")
plt.show()

# =========================
# SIMPAN MODEL
# =========================
model.save("model_emotion.keras")  # 🔥 modern format
print("✅ Model disimpan!")
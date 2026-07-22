import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# ==============================
# Load Model
# ==============================

MODEL_PATH = "model/model_betta_final.keras"
model = load_model(MODEL_PATH)
# ==============================
# Class Labels
# ==============================

CLASS_NAMES = [
    "Dumbo Ear",
    "Halfmoon",
    "Plakat"
]

# ==============================
# Fish Information
# ==============================

FISH_INFO = {

    "Dumbo Ear": {
        "icon": "🐘",
        "description": (
            "Cupang Dumbo Ear merupakan salah satu jenis ikan cupang hias "
            "yang memiliki ciri khas berupa sirip dada berukuran besar "
            "menyerupai telinga gajah (dumbo). Jenis ini sangat populer di "
            "kalangan pecinta ikan hias karena memiliki bentuk tubuh yang "
            "indah, gerakan berenang yang anggun, serta variasi warna yang "
            "beragam."
        ),
        "characteristics": [
            "Sirip dada besar menyerupai telinga gajah.",
            "Gerakan berenang anggun dan elegan.",
            "Memiliki kombinasi warna yang beragam.",
            "Populer sebagai ikan hias dan ikan kontes."
        ]
    },

    "Halfmoon": {
        "icon": "🌙",
        "description": (
            "Cupang Halfmoon memiliki bukaan ekor hingga sekitar "
            "180 derajat sehingga membentuk setengah lingkaran seperti "
            "bulan purnama."
        ),
        "characteristics": [
            "Ekor membuka hingga sekitar 180°.",
            "Sirip panjang dan simetris.",
            "Gerakan berenang lembut.",
            "Sering digunakan dalam kontes."
        ]
    },

    "Plakat": {
        "icon": "⚔️",
        "description": (
            "Cupang Plakat memiliki sirip pendek dengan tubuh yang "
            "lebih kekar. Jenis ini terkenal aktif dan agresif."
        ),
        "characteristics": [
            "Sirip pendek.",
            "Tubuh lebih kokoh.",
            "Gerakan cepat.",
            "Daya tahan tubuh baik."
        ]
    }

}

# ==============================
# Image Preprocessing
# ==============================

def preprocess_image(image_path):

    image = Image.open(image_path).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image).astype("float32") / 255.0
    image = np.expand_dims(image, axis=0)

    return image


# ==============================
# Prediction
# ==============================
THRESHOLD = 0.70
def predict_image(image_path):
    image = preprocess_image(image_path)
    prediction = model.predict(image, verbose=0)[0]
    confidence = float(np.max(prediction))
    class_index = int(np.argmax(prediction))

    probabilities = {
        CLASS_NAMES[i]: round(float(prediction[i] * 100), 2)
        for i in range(len(CLASS_NAMES))
    }

    # ===================================================
    # Tidak Dikenali
    # ===================================================

    if confidence < THRESHOLD:

        return {

            "class": "Tidak Dikenali",

            "icon": "❓",

            "confidence": round(confidence * 100, 2),

            "status": "Keyakinan Rendah",

            "description": (
                "Sistem tidak dapat mengenali gambar sebagai salah satu "
                "jenis ikan cupang yang didukung. Pastikan gambar merupakan "
                "ikan cupang Dumbo Ear, Halfmoon, atau Plakat."
            ),

            "characteristics": [

                "Gunakan gambar ikan cupang yang jelas.",

                "Pastikan hanya terdapat satu ikan pada gambar.",

                "Hindari gambar buram atau terlalu gelap.",

                "Sistem hanya mengenali Dumbo Ear, Halfmoon, dan Plakat."

            ],

            "probabilities": probabilities

        }

    # ===================================================
    # Jika dikenali
    # ===================================================

    predicted_class = CLASS_NAMES[class_index]

    info = FISH_INFO[predicted_class]

    if confidence >= 0.90:
        status = "Sangat Yakin"
    elif confidence >= 0.80:
        status = "Yakin"
    else:
        status = "Cukup Yakin"

    return {

        "class": predicted_class,
        "icon": info["icon"],
        "confidence": round(confidence * 100, 2),
        "status": status,
        "description": info["description"],
        "characteristics": info["characteristics"],
        "probabilities": probabilities
    }
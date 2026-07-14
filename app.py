from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils import predict_image
import os

# ==========================================
# Flask Configuration
# ==========================================

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Membuat folder upload jika belum ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# Helper Function
# ==========================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

# ==========================================
# Home Page
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# About Page
# ==========================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==========================================
# Prediction
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    # Tidak ada file yang dipilih
    if "image" not in request.files:
        return render_template(
            "index.html",
            error="Silakan pilih gambar terlebih dahulu."
        )

    file = request.files["image"]

    # Nama file kosong
    if file.filename == "":
        return render_template(
            "index.html",
            error="Silakan pilih gambar terlebih dahulu."
        )

    # Format file tidak sesuai
    if not allowed_file(file.filename):
        return render_template(
            "index.html",
            error="Format file harus JPG, JPEG, atau PNG."
        )

    # Simpan file
    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(filepath)

    # Prediksi
    result = predict_image(filepath)

    # Kirim ke halaman hasil
    return render_template(
        "result.html",
        image=filename,
        result=result
    )


# ==========================================
# Run Flask
# ==========================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
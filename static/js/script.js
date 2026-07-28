document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector(".navbar");
    const imageInput = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const dropArea = document.getElementById("dropArea");

    console.log(messageBox);
    /* ===========================
    Navbar Scroll
    =========================== */

    window.addEventListener("scroll", () => {

        if (window.scrollY > 50) {

            navbar.style.background = "rgba(8,28,58,.95)";
            navbar.style.boxShadow = "0 10px 30px rgba(0,0,0,.15)";

        } else {

            navbar.style.background = "rgba(8,20,45,.35)";
            navbar.style.boxShadow = "none";

        }

    });

    /* ===========================
    Image Preview
    =========================== */

    if (imageInput) {

        imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    const allowedTypes = [
        "image/jpeg",
        "image/jpg",
        "image/png"
    ];

    if (!allowedTypes.includes(file.type)) {
        messageBox.innerHTML = "⚠️ Format file tidak didukung. Gunakan JPG, JPEG, atau PNG.";
        messageBox.style.display = "block";
        this.value = "";
        preview.style.display = "none";
        return;
    }

    messageBox.style.display = "none";

    const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";

        };

        reader.readAsDataURL(file);

    });

    }

    /* ===========================
       Drag & Drop
    =========================== */

    if (dropArea) {

        ["dragenter", "dragover"].forEach(eventName => {

            dropArea.addEventListener(eventName, e => {

                e.preventDefault();
                dropArea.classList.add("drag-active");

            });

        });

        ["dragleave", "drop"].forEach(eventName => {

            dropArea.addEventListener(eventName, e => {

                e.preventDefault();
                dropArea.classList.remove("drag-active");

            });

        });

        dropArea.addEventListener("drop", e => {

            const files = e.dataTransfer.files;

            if (!files.length) return;

            imageInput.files = files;

            const reader = new FileReader();

            reader.onload = function (event) {

                preview.src = event.target.result;
                preview.style.display = "block";

            };

            reader.readAsDataURL(files[0]);

        });

    }

    /* ===========================
       Smooth Scroll
    =========================== */

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (!target) return;

            e.preventDefault();

            target.scrollIntoView({

                behavior: "smooth"

            });

        });

    });

    /* ===========================
       Fade Animation
    =========================== */

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, {

        threshold: 0.15

    });

    document.querySelectorAll(
        ".feature-card, .glass-card, .tech-card, .step-card, .stat-box, .cta-card"
    ).forEach(element => {

        element.classList.add("hidden");
        observer.observe(element);

    });

});

/* ===========================
   Validasi Upload
=========================== */

const uploadForm = document.getElementById("uploadForm");
const messageBox = document.getElementById("message");

if (uploadForm) {
    uploadForm.addEventListener("submit", function (e) {

        if (imageInput.files.length === 0) {

            e.preventDefault();
            
            messageBox.innerHTML = "Silakan pilih gambar terlebih dahulu.";

            messageBox.style.display = "block";

            return;

        }
        messageBox.style.display = "none";
    });

}
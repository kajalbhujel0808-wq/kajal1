import os
import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def index():
    resume = None
    corrected = None

    if request.method == "POST":
        fields = [
            "furigana", "name", "birthday", "gender",
            "address", "phone", "email",
            "education1_year", "education1_month",
            "education1_school", "education1_type",
            "education2_year", "education2_month",
            "education2_school", "education2_type",
            "education3_year", "education3_month",
            "education3_school", "education3_type",
            "work", "qualification", "self_pr",
            "motivation", "hope"
        ]

        resume = {
            field: request.form.get(field, "").strip()
            for field in fields
        }

        # Photo upload
        photo = request.files.get("photo")
        photo_path = ""

        if photo and photo.filename:
            if allowed_file(photo.filename):
                extension = secure_filename(
                    photo.filename
                ).rsplit(".", 1)[1].lower()

                filename = f"{uuid.uuid4().hex}.{extension}"
                photo.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        filename
                    )
                )
                photo_path = f"uploads/{filename}"
            else:
                return (
                    "JPG, JPEG, PNG वा WEBP फोटो मात्र upload गर्नुहोस्।",
                    400
                )

        resume["photo"] = photo_path

        corrected = {
            "self_pr": resume["self_pr"],
            "motivation": resume["motivation"]
        }

    return render_template(
        "index.html",
        resume=resume,
        corrected=corrected
    )


@app.errorhandler(413)
def file_too_large(error):
    return "फोटोको साइज 5 MB भन्दा कम हुनुपर्छ।", 413


if __name__ == "__main__":
    app.run(debug=True)
from flask import Blueprint, send_from_directory

uploads = Blueprint("uploads", __name__, template_folder="templates")


@uploads.route("/<filename>")
def send_file(filename, UPLOAD_FOLDER="Uploads"):
    return send_from_directory(UPLOAD_FOLDER, filename)

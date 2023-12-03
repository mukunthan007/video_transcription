from flask import request, Blueprint, render_template, current_app, send_file
from werkzeug.utils import secure_filename
import random
import threading
import os
from app.modelling import PreprocessinAudio
from app.modelling import WhisperPrediction
import json
import pathlib


get_translation_api = Blueprint("whisperai", __name__)
get_progression_api = Blueprint("whisperai/progress/<int:thread_id>", __name__)
get_subtitles_api = Blueprint("whisperai/sub/<int:thread_id>", __name__)

ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "wmv", "avchd", "webm"}

exporting_threads = {}


class ExportingThread(threading.Thread):
    def __init__(self):
        self.progress = False
        self.output = ""
        self.stream = WhisperPrediction()
        super().__init__()

    def run(self):
        preprocessed_audio = PreprocessinAudio().seperate_video_to_audio(self.file_path)
        extracted_data = self.stream.transcribe_audio(preprocessed_audio)
        self.output = extracted_data
        self.progress = True


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_request(request: request):
    if "file" not in request.files:
        print("infile")
        return render_template("file_not_supported.html"), 500
    file = request.files["file"]
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        return render_template("500.html"), 500
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file.save(
            os.path.join(os.getcwd(), current_app.config["UPLOAD_FOLDER"], filename)
        )
        return filename


@get_translation_api.route("/whisperai", methods=["POST"])
def transcribe_video():
    global exporting_threads
    thread_id = random.randint(0, 10000)
    file_path = get_request(request)
    ex_thread = ExportingThread()
    ex_thread.file_path = file_path
    exporting_threads[thread_id] = ex_thread
    exporting_threads[thread_id].start()
    return str(thread_id)


@get_progression_api.route("/whisperai/progress/<int:thread_id>", methods=["GET"])
def check_and_send_data(thread_id):
    global exporting_threads
    print(exporting_threads[thread_id].stream.output_result)
    return {
        "status": exporting_threads[thread_id].progress,
        "output_text": exporting_threads[thread_id].stream.output_result,
    }


@get_subtitles_api.route("/whisperai/sub/<int:thread_id>", methods=["GET"])
def send_sub(thread_id):
    global exporting_threads
    send_vtt = send_file(exporting_threads[thread_id].output, as_attachment=True)
    # pathlib.Path(send_vtt).unlink()
    del exporting_threads[thread_id]
    return send_vtt

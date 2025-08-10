# Author:      Miguel Gonzalez Almonte  # Created:     2025-05-24  # File:        server_flask.py  # Description: Flask backend server  
# server_flask.py
# Flask backend server

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

@app.route("/log", methods=["POST"])
def log_event():
    data = request.get_json()
    with open("logs/launch.log", "a", encoding="utf-8") as f:
        f.write(f"{data}\n")
    return jsonify({"status": "logged"})

@app.route("/widgets", methods=["GET"])
def list_widgets():
    return jsonify({
        "qt": ["QPushButton", "QSlider", "QCheckBox"],
        "tk": ["Button", "Scale", "Checkbutton"]
    })

if __name__ == "__main__":
    app.run(debug=True)

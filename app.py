from flask import Flask, jsonify, send_from_directory, request
import json
from speak import render_tts, optimize_text

app = Flask(__name__, static_folder="static")

with open("fixtures.json") as f:
    FIXTURES = json.load(f)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/fixtures")
def fixtures():
    return jsonify(FIXTURES)

@app.route("/speak/<int:fid>/<mode>")
def speak(fid, mode):
    fx = next((f for f in FIXTURES if f["id"] == fid), None)
    if not fx:
        return jsonify({"error": "not found"}), 404

    text = fx["raw"] if mode == "baseline" else optimize_text(fx["raw"])
    out_path = f"static/clips/{fid}_{mode}_live.wav"
    render_tts(text, out_path)
    return jsonify({"url": f"/clips/{fid}_{mode}_live.wav", "text": text})

@app.route("/clips/<path:filename>")
def clips(filename):
    return send_from_directory("static/clips", filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
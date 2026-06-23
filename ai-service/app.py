from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import os

app = Flask(__name__)
CORS(app)

# Create uploads folder if it doesn't exist
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO model once
model = YOLO("yolo11n.pt")


@app.route("/")
def home():
    return "AutoFocus AI Service Running"


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Run prediction
    results = model(filepath)

    predictions = []

    for result in results:
        for box in result.boxes:
            predictions.append({
                "class_id": int(box.cls[0]),
                "confidence": float(box.conf[0])
            })

    return jsonify({
        "message": "Prediction successful",
        "detections": predictions
    })


if __name__ == "__main__":
    app.run(debug=True)
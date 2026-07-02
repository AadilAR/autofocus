from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PREDICTION_FOLDER = "predictions"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICTION_FOLDER, exist_ok=True)

# Load YOLO model
model = YOLO("models/best.pt")


@app.route("/")
def home():
    return jsonify({
        "message": "🚗 AutoFocus AI Service Running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # Run prediction
    results = model.predict(
        source=image_path,
        save=True,
        project=PREDICTION_FOLDER,
        name="results",
        exist_ok=True
    )

    detections = []

    for result in results:

        print("Prediction saved in:", result.save_dir)

        for box in result.boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "confidence": round(float(box.conf), 4),
                "bbox": [float(x) for x in box.xyxy[0].tolist()]
            })

    # Build image path
    prediction_image = os.path.join(
        PREDICTION_FOLDER,
        "results",
        image.filename
    )

    return jsonify({
        "message": "Prediction completed",
        "detections": detections,
        "predictionImage": prediction_image.replace("\\", "/")
    })


@app.route("/predictions/<filename>")
def prediction_image(filename):
    return send_from_directory(
        os.path.join(PREDICTION_FOLDER, "results"),
        filename
    )


if __name__ == "__main__":
    app.run(port=5001, debug=True)
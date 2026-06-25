from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Create uploads folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load YOLO model
# Load trained AutoFocus damage detection model
MODEL_PATH = "runs/detect/runs/autofocus_damage_model-2/weights/best.pt"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = YOLO(MODEL_PATH)


@app.route("/")
def home():
    return jsonify({
        "message": "AutoFocus AI Service Running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    # Validate request
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image uploaded."
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected."
        }), 400

    # Save uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Run YOLO prediction
    results = model(filepath)

    detections = []

    for result in results:

        class_names = result.names

        for box in result.boxes:

            class_id = int(box.cls[0])

            detections.append({

                "damageType": class_names[class_id],

                "confidence": round(float(box.conf[0]), 2),

                "boundingBox": {
                    "x1": round(float(box.xyxy[0][0]), 2),
                    "y1": round(float(box.xyxy[0][1]), 2),
                    "x2": round(float(box.xyxy[0][2]), 2),
                    "y2": round(float(box.xyxy[0][3]), 2)
                },

                # Future AI modules
                "severity": None,
                "estimatedCost": None,
                "recommendedWorkshop": None
            })

    return jsonify({

        "success": True,

        "message": "Prediction completed successfully.",

        "imageName": file.filename,

        "predictionTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "totalDetections": len(detections),

        "detections": detections
    })


if __name__ == "__main__":
    app.run(debug=True)
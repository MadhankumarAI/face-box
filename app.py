from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from fer import FER

app = Flask(__name__)
CORS(app, resources={r"/detect_emotion": {"origins": "http://localhost:5173"}})

detector = FER(mtcnn=True)  # More accurate face detection

@app.route("/detect_emotion", methods=["POST"])
def detect_emotion():
    data = request.json
    if "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    # Decode base64 image
    img_data = base64.b64decode(data["image"].split(",")[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Detect emotions
    results = detector.detect_emotions(frame)

    if not results:
        return jsonify({"message": "No face detected"}), 200

    response = []
    for result in results:
        (x, y, w, h) = result["box"]
        emotions = result["emotions"]
        top_emotion = max(emotions, key=emotions.get)
        response.append({
            "box": {"x": x, "y": y, "w": w, "h": h},
            "emotion": top_emotion,
            "confidence": round(emotions[top_emotion], 2)
        })

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

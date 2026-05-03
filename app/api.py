import os
import pandas as pd
from flask import Flask, request, jsonify

from app.model_handler import load_model, load_metadata, ModelNotLoadedError

app = Flask(__name__)

MODEL = None
METADATA = {}
MODEL_VERSION = "unknown"
FEATURE_NAMES = []


def init_model():
    global MODEL, METADATA, MODEL_VERSION, FEATURE_NAMES
    try:
        MODEL = load_model()
        METADATA = load_metadata()
        MODEL_VERSION = METADATA.get("model_version", "v1")
        FEATURE_NAMES = METADATA.get("feature_names", [])
        app.logger.info("Model loaded successfully")
    except ModelNotLoadedError as e:
        app.logger.error(f"Model load error: {e}")
        MODEL = None
    except Exception as e:
        app.logger.error(f"Unexpected error loading model: {e}")
        MODEL = None


@app.route("/health", methods=["GET"])
def health():
    is_healthy = MODEL is not None
    return jsonify({
        "healthy": is_healthy,
        "status": "ok" if is_healthy else "error",
        "model_version": MODEL_VERSION
    }), 200 if is_healthy else 500


@app.route("/predict", methods=["POST"])
def predict():
    if MODEL is None:
        return jsonify({"error": "model not loaded"}), 500

    try:
        payload = request.get_json()

        if payload is None:
            return jsonify({"error": "empty JSON payload"}), 400

        if not isinstance(payload, dict):
            return jsonify({"error": "JSON payload must be an object"}), 400

        missing_features = [col for col in FEATURE_NAMES if col not in payload]
        if missing_features:
            return jsonify({
                "error": "missing required features",
                "missing_features": missing_features
            }), 400

        input_df = pd.DataFrame([payload])
        input_df = input_df[FEATURE_NAMES]

        probability = float(MODEL.predict_proba(input_df)[:, 1][0])
        prediction = int(probability >= 0.5)

        return jsonify({
            "prediction": prediction,
            "probability": round(probability, 4),
            "model_version": MODEL_VERSION
        }), 200

    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": "prediction failed"}), 500


init_model()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
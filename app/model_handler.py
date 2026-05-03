import os
import json
import joblib

ARTIFACTS_DIR = "models/artifacts"
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(ARTIFACTS_DIR, "model.pkl"))
METADATA_PATH = os.getenv("METADATA_PATH", os.path.join(ARTIFACTS_DIR, "metadata.json"))


class ModelNotLoadedError(Exception):
    pass


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise ModelNotLoadedError(f"Model file not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    return model


def load_metadata():
    if not os.path.exists(METADATA_PATH):
        return {}
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score

DATA_PATH = "default_of_credit_card_clients.csv"
ARTIFACTS_DIR = "models/artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "model.pkl")
METADATA_PATH = os.path.join(ARTIFACTS_DIR, "metadata.json")

TARGET_COL = "default.payment.next.month"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    if "ID" in df.columns:
        df = df.drop(columns=["ID"])
    return df


def train_model(df: pd.DataFrame):
    df = preprocess(df)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_valid)
    y_proba = model.predict_proba(X_valid)[:, 1]

    metrics = {
        "f1": round(f1_score(y_valid, y_pred), 4),
        "precision": round(precision_score(y_valid, y_pred), 4),
        "recall": round(recall_score(y_valid, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_valid, y_proba), 4)
    }

    feature_names = list(X.columns)

    return model, metrics, feature_names


def save_artifacts(model, metrics: dict, feature_names: list):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    metadata = {
        "model_version": "v1",
        "metrics": metrics,
        "feature_names": feature_names
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def main():
    df = load_data(DATA_PATH)
    model, metrics, feature_names = train_model(df)
    save_artifacts(model, metrics, feature_names)

    print("Model saved to:", MODEL_PATH)
    print("Metadata saved to:", METADATA_PATH)
    print("Metrics:", metrics)


if __name__ == "__main__":
    main()
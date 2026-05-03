import json
from app.api import app


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code in (200, 500)

    data = response.get_json()
    assert "status" in data
    assert "model_version" in data
    assert "healthy" in data


def test_predict_success():
    client = app.test_client()

    payload = {
        "LIMIT_BAL": 20000,
        "SEX": 2,
        "EDUCATION": 2,
        "MARRIAGE": 1,
        "AGE": 34,
        "PAY_0": 0,
        "PAY_2": 0,
        "PAY_3": 0,
        "PAY_4": 0,
        "PAY_5": 0,
        "PAY_6": 0,
        "BILL_AMT1": 3913,
        "BILL_AMT2": 3102,
        "BILL_AMT3": 689,
        "BILL_AMT4": 0,
        "BILL_AMT5": 0,
        "BILL_AMT6": 0,
        "PAY_AMT1": 0,
        "PAY_AMT2": 689,
        "PAY_AMT3": 0,
        "PAY_AMT4": 0,
        "PAY_AMT5": 0,
        "PAY_AMT6": 0
    }

    response = client.post(
        "/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 200

    data = response.get_json()
    assert "prediction" in data
    assert "probability" in data
    assert "model_version" in data
    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1


def test_predict_missing_features():
    client = app.test_client()

    payload = {
        "LIMIT_BAL": 20000,
        "SEX": 2
    }

    response = client.post(
        "/predict",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
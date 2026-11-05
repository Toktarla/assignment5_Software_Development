from fastapi.testclient import TestClient

from sentiment_app.api import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze():
    response = client.post(
        "/api/analyze",
        json={"text": "Переводы обложили налогом — это лишнее."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["label"] == "negative"
    assert body["topic"] == "mobile_transfer_tax"


def test_empty_body_is_rejected():
    empty = client.post("/api/analyze", json={"text": ""})
    spaces = client.post("/api/analyze", json={"text": "   "})
    assert empty.status_code == 422
    assert spaces.status_code == 400

from fastapi.testclient import TestClient
from src.app.inference import app
import requests

TEST_FILE = "data/test_x.csv"
client = TestClient(app)


def test_create_request():
    files = {"file": open(TEST_FILE, "rb")}
    response = client.post(
        "/invocation",
        files=files,
    )

    url = "http://192.168.0.157:8003/invocation"
    resp = requests.post(url=url, files=files)

    assert response.status_code == 200
    assert resp.status_code == 200
    assert response.json() == resp.json()

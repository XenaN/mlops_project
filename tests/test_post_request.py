import requests

TEST_FILE = "tests/data/test_x.csv"


def test_create_request():
    files = {"file": open(TEST_FILE, "rb")}
    url = "http://192.168.0.176:8003/invocation"
    resp = requests.post(url=url, files=files)
    result = resp.json()

    assert resp.status_code == 200
    assert type(result) is list
    assert type(result[0]) is float

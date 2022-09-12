from starlette.testclient import TestClient

from shortener.main import app

client = TestClient(app)


def test_get_url():
    response = client.get("/url")
    assert response.status_code == 200

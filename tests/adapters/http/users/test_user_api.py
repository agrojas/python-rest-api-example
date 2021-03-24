from fastapi.testclient import TestClient
from main import api

client = TestClient(api)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

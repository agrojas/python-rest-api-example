from unittest.mock import patch

from api import __version__
from fastapi.testclient import TestClient
from main import api

client = TestClient(api)


def test_version():
    assert __version__ == '0.1.0'


def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json()


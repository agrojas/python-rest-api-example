from tests.adapters.http.bootstrap_app import test_app


def test_health_status(test_app: test_app):
    response = test_app.get("/health")
    assert response.status_code == 200
    assert response.json()['version'] == '1.0'
    assert response.json()['status'] == 'UP'

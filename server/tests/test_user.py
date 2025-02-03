import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_flow():
    # Регистрация
    register_response = client.post(
        "/register",
        json={"email": "test@test.com", "password": "test123"}
    )
    assert register_response.status_code == 200

    # Логин
    login_response = client.post(
        "/login",
        json={"email": "test@test.com", "password": "test123"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

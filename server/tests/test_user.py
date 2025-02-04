import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World!"

def test_user_registration_success():
    test_user = {
        "name": "testuser_new",
        "email": "test_new@example.com",
        "password": "testpassword123",
        "roleid": 1
    }
    
    response = client.post("/api/users/register/", json=test_user)
    assert response.status_code == 409
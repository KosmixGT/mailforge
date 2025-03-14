import pytest
from fastapi.testclient import TestClient
from app.main import app
from services.auth.app.application.dto.user_dto import UserCreateDTO

client = TestClient(app=app)

def test_user_registration_success():
    test_user = UserCreateDTO(
        name="testuser_new",
        email="test_new@example.com",
        password="testpassword123",
        role_id=1
    )
    
    response = client.post("/api/v1/users/register/", json=test_user.model_dump())
    assert response.status_code == 400

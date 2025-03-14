from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_history_get_by_id():
    response = client.get("/api/v1/history/27")
    assert response.status_code == 200
    assert response.json().get("delivery_status_id") == 2

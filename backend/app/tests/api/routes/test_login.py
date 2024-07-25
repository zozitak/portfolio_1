from fastapi.testclient import TestClient

from app.main import app
from app.base.config import settings

client = TestClient(app)

def test_api_login():
    response = client.get(settings.API_STR)
    assert response.status_code == 204
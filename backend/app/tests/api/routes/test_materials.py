from fastapi.testclient import TestClient

from app.main import app
from app.base.config import settings

client = TestClient(app)

def test_api_users():
    response = client.get(settings.API_STR+"/materials")
    assert response.status_code == 204
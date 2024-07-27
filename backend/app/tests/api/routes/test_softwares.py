from fastapi.testclient import TestClient

from app.main import app
from app.base.config import settings

client = TestClient(app)

def test_api_softwares():
    response = client.get(settings.API_STR+"/softwares")
    assert response.status_code == 204
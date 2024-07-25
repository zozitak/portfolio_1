from fastapi.testclient import TestClient
from app.base.config import settings

from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 204

def test_app_properties():
    assert app.title == settings.APP_NAME
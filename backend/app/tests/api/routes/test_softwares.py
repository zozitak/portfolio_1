import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.base.config import settings
from app.tests.utils.software import create_random_software


def test_create_software(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Foo"}
    response = client.post(
        f"{settings.API_STR}/softwares/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_software(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    software = create_random_software(db)
    response = client.get(
        f"{settings.API_STR}/softwares/{software.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == software.name
    assert content["id"] == str(software.id)


def test_read_software_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_STR}/softwares/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Software not found"


def test_read_software_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    software = create_random_software(db)
    response = client.get(
        f"{settings.API_STR}/softwares/{software.id}"
    )
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "Not authenticated"


def test_read_softwares(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_software(db)
    create_random_software(db)
    response = client.get(
        f"{settings.API_STR}/softwares/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_software(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    software = create_random_software(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_STR}/softwares/{software.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == str(software.id)


def test_update_software_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_STR}/softwares/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Software not found"


def test_update_software_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    software = create_random_software(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_STR}/softwares/{software.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_software(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    software = create_random_software(db)
    response = client.delete(
        f"{settings.API_STR}/softwares/{software.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Software deleted successfully"


def test_delete_software_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_STR}/softwares/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Software not found"


def test_delete_software_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_software(db)
    response = client.delete(
        f"{settings.API_STR}/softwares/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
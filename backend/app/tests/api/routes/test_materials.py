import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.base.config import settings
from app.tests.utils.material import create_random_material


def test_create_material(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Foo", "description": "Bar"}
    response = client.post(
        f"{settings.API_STR}/materials/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content


def test_read_material(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    material = create_random_material(db)
    response = client.get(
        f"{settings.API_STR}/materials/{material.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == material.name
    assert content["description"] == material.description
    assert content["id"] == str(material.id)


def test_read_material_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_STR}/materials/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Material not found"


def test_read_material_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    material = create_random_material(db)
    response = client.get(
        f"{settings.API_STR}/materials/{material.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_materials(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_material(db)
    create_random_material(db)
    response = client.get(
        f"{settings.API_STR}/materials/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_material(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    material = create_random_material(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_STR}/materials/{material.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == str(material.id)


def test_update_material_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_STR}/materials/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_update_material_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    material = create_random_material(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_STR}/items/{material.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_material(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    material = create_random_material(db)
    response = client.delete(
        f"{settings.API_STR}/materials/{material.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Material deleted successfully"


def test_delete_material_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/materials/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Material not found"


def test_delete_material_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_material(db)
    response = client.delete(
        f"{settings.API_STR}/materials/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
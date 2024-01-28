from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from models import Menu
from schemas import MenuCreate, MenuUpdate


def test_get_menu(client: TestClient, db: Session):
    test_menu = Menu(id=uuid4(), title="Test Menu", description="Test Description")
    db.add(test_menu)
    db.commit()
    db.refresh(test_menu)

    response = client.get(f"/api/v1/menus/{test_menu.id}")
    assert response.status_code == 200
    menu_data = response.json()
    assert menu_data["title"] == test_menu.title
    assert menu_data["description"] == test_menu.description


def test_get_menus_list(client: TestClient, db: Session):
    for i in range(3):
        test_menu = Menu(id=uuid4(), title=f"Test Menu {i}", description=f"Test Description {i}")
        db.add(test_menu)
    db.commit()

    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    menus_data = response.json()
    assert len(menus_data) == 3


def test_create_menu(client: TestClient, db: Session):
    new_menu = MenuCreate(title="New Menu", description="New Description")
    response = client.post("/api/v1/menus", json=new_menu.model_dump())
    assert response.status_code == 201
    created_menu = response.json()
    assert created_menu["title"] == new_menu.title
    assert created_menu["description"] == new_menu.description


def test_update_menu(client: TestClient, db: Session):
    test_menu = Menu(id=uuid4(), title="Test Menu", description="Test Description")
    db.add(test_menu)
    db.commit()
    db.refresh(test_menu)

    updated_menu = MenuUpdate(title="Updated Menu", description="Updated Description")
    response = client.patch(f"/api/v1/menus/{test_menu.id}", json=updated_menu.model_dump())
    assert response.status_code == 200
    updated_menu_data = response.json()
    assert updated_menu_data["title"] == updated_menu.title
    assert updated_menu_data["description"] == updated_menu.description


def test_delete_menu(client: TestClient, db: Session):
    test_menu = Menu(id=uuid4(), title="Test Menu", description="Test Description")
    db.add(test_menu)
    db.commit()
    db.refresh(test_menu)

    response = client.delete(f"/api/v1/menus/{test_menu.id}")
    assert response.status_code == 200
    message = response.json()
    assert message["message"] == "Меню удалено"

    response = client.get(f"/api/v1/menus/{test_menu.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from main import app
from models import Menu, Submenu
from schemas import SubmenuCreate, SubmenuUpdate


def test_get_submenus_list(client: TestClient, db: Session):
    # Create a menu and submenus for testing
    menu_id = str(uuid4())
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    submenu1 = Submenu(id=str(uuid4()), title="Submenu 1", description="Test Submenu 1", menu_id=menu_id)
    submenu2 = Submenu(id=str(uuid4()), title="Submenu 2", description="Test Submenu 2", menu_id=menu_id)
    db.add(menu)
    db.add(submenu1)
    db.add(submenu2)
    db.commit()

    # Make a request to the get_submenus_list endpoint
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == submenu1.title
    assert data[0]["description"] == submenu1.description
    assert data[1]["title"] == submenu2.title
    assert data[1]["description"] == submenu2.description

    # Test with a non-existent menu ID
    non_existent_menu_id = str(uuid4())
    response = client.get(f"/api/v1/menus/{non_existent_menu_id}/submenus")
    assert response.status_code == 404
    assert response.json() == {"detail": "Меню не найдено"}


def test_get_submenu(client: TestClient, db: Session):
    # Create a menu and a submenu for testing
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Description", menu_id=menu_id)
    db.add(menu)
    db.add(submenu)
    db.commit()

    # Make a request to the get_submenu endpoint
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == submenu.title
    assert data["description"] == submenu.description


def test_create_submenu(client: TestClient, db: Session):
    # Create a menu for testing
    menu_id = str(uuid4())
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu)
    db.commit()

    submenu_id = str(uuid4())
    submenu_data = SubmenuCreate(title="Test Submenu", description="Test Description", menu_id=menu_id)

    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu_data.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == submenu_data.title
    assert data["description"] == submenu_data.description
    assert data["menu_id"] == menu_id


def test_update_submenu(client: TestClient, db: Session):
    # Create a menu and a submenu for testing
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Description", menu_id=menu_id)
    db.add(menu)
    db.add(submenu)
    db.commit()

    # Update the submenu
    updated_submenu_data = SubmenuUpdate(title="Updated Submenu", description="Updated Description")

    # Make a request to the update_submenu endpoint
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=updated_submenu_data.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_submenu_data.title
    assert data["description"] == updated_submenu_data.description

def test_delete_submenu(client: TestClient, db: Session):
    # Create a menu and a submenu for testing
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Description", menu_id=menu_id)
    db.add(menu)
    db.add(submenu)
    db.commit()

    # Make a request to the delete_submenu endpoint
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200

    # Check that the submenu was deleted
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()
    assert submenu is None

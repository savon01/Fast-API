from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from models import Menu, Submenu, Dish
from schemas import MenuCreate, MenuUpdate
from three import get_menus_with_counts


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


def test_get_menus_with_counts(client: TestClient, db: Session):
    # Создаем тестовые меню, подменю и блюда
    menu_id = str(uuid4())
    menu1 = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu1)
    db.commit()
    db.refresh(menu1)

    submenu_id = str(uuid4())
    submenu1 = Submenu(id=submenu_id, title="Test Submenu", description="Test Submenu Description", menu_id=menu_id)
    db.add(submenu1)
    db.commit()
    db.refresh(submenu1)

    dish_id1 = str(uuid4())
    dish1 = Dish(id=dish_id1, title="Test Dish 1", description="Test Description", price="10.99", submenu_id=submenu_id)
    db.add(dish1)
    db.commit()
    db.refresh(dish1)

    dish_id2 = str(uuid4())
    dish2 = Dish(id=dish_id2, title="Test Dish 2", description="Test Description", price="10.99", submenu_id=submenu_id)
    db.add(dish2)
    db.commit()
    db.refresh(dish2)

    menus_with_counts_before_deletion = get_menus_with_counts(db)

    assert any(menu['id'] == menu_id for menu in menus_with_counts_before_deletion)

    db.query(Dish).filter(Dish.submenu_id == submenu_id).delete()
    db.commit()

    db.query(Submenu).filter(Submenu.menu_id == menu_id).delete()
    db.commit()

    db.query(Menu).filter(Menu.id == menu_id).delete()
    db.commit()

    menus_with_counts_after_deletion = get_menus_with_counts(db)


    assert not any(menu['id'] == menu_id for menu in menus_with_counts_after_deletion)

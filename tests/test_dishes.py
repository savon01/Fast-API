from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from uuid import uuid4

from models import Dish, Menu, Submenu
from schemas import DishUpdate, DishCreate


def create_test_menu_submenu_dish(db: Session):
    menu_id = str(uuid4())
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu)
    db.commit()
    db.refresh(menu)

    submenu_id = str(uuid4())
    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Submenu Description", menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)

    dish_id = str(uuid4())
    dish = Dish(id=dish_id, title="Test Dish", description="Test Description", price="10.99", submenu_id=submenu_id)
    db.add(dish)
    db.commit()
    db.refresh(dish)

    return menu, submenu, dish


def cleanup_test_data(db: Session, menu: Menu, submenu: Submenu, dish: Dish):
    db.query(Dish).filter(Dish.id == str(dish.id)).delete()
    db.query(Submenu).filter(Submenu.id == str(submenu.id)).delete()
    db.query(Menu).filter(Menu.id == str(menu.id)).delete()
    db.commit()


def test_get_dish(client: TestClient, db: Session):
    menu, submenu, dish = create_test_menu_submenu_dish(db)

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}")
    assert response.status_code == 200
    dish_response = response.json()
    assert dish_response["title"] == dish.title
    assert dish_response["description"] == dish.description
    assert dish_response["price"] == str(dish.price)

    cleanup_test_data(db, menu, submenu, dish)


def create_test_menu_submenu_dishes(db: Session, menu_id: str, submenu_id: str):
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu)
    db.commit()
    db.refresh(menu)

    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Submenu Description", menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)

    dish1 = Dish(id=str(uuid4()), title="Test Dish 1", description="Test Description 1", price="10.99", submenu_id=submenu_id)
    dish2 = Dish(id=str(uuid4()), title="Test Dish 2", description="Test Description 2", price="12.99", submenu_id=submenu_id)
    db.add_all([dish1, dish2])
    db.commit()

    return menu, submenu, [dish1, dish2]


def test_get_dishes_list(client: TestClient, db: Session):
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    menu, submenu, dishes = create_test_menu_submenu_dishes(db, menu_id, submenu_id)

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    dishes_response = response.json()
    assert len(dishes_response) == len(dishes)
    for dish, dish_response in zip(dishes, dishes_response):
        assert dish_response["title"] == dish.title
        assert dish_response["description"] == dish.description
        assert dish_response["price"] == str(dish.price)

    db.query(Dish).filter(Dish.submenu_id == submenu_id).delete()
    db.query(Submenu).filter(Submenu.id == submenu_id).delete()
    db.query(Menu).filter(Menu.id == menu_id).delete()
    db.commit()


def create_test_menu_submenu(db: Session, menu_id: str, submenu_id: str):

    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu)
    db.commit()
    db.refresh(menu)


    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Submenu Description", menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)

    return menu, submenu


def test_create_dish(client: TestClient, db: Session):
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    menu, submenu = create_test_menu_submenu(db, menu_id, submenu_id)

    dish_create = DishCreate(title="Test Dish", description="Test Description", price="10.99")

    response = client.post(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        json=dish_create.model_dump()
    )
    assert response.status_code == 201
    dish_response = response.json()
    assert dish_response["title"] == dish_create.title
    assert dish_response["description"] == dish_create.description
    assert dish_response["price"] == str(dish_create.price)
    assert dish_response["submenu_id"] == submenu_id

    db_dish = db.query(Dish).filter_by(id=dish_response["id"]).first()
    assert db_dish is not None
    assert db_dish.title == dish_create.title
    assert db_dish.description == dish_create.description
    assert db_dish.price == dish_create.price
    assert db_dish.submenu_id == submenu_id

    db.query(Dish).filter(Dish.id == dish_response["id"]).delete()
    db.query(Submenu).filter(Submenu.id == submenu_id).delete()
    db.query(Menu).filter(Menu.id == menu_id).delete()
    db.commit()


def create_test_menu_submenu_dish2(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu)
    db.commit()
    db.refresh(menu)

    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Submenu Description", menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)

    dish = Dish(id=dish_id, title="Test Dish", description="Test Description", price="10.99", submenu_id=submenu_id)
    db.add(dish)
    db.commit()
    db.refresh(dish)

    return menu, submenu, dish


def test_update_dish(client: TestClient, db: Session):
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    dish_id = str(uuid4())
    menu, submenu, dish = create_test_menu_submenu_dish2(db, menu_id, submenu_id, dish_id)

    updated_dish = DishUpdate(title="Updated Dish", description="Updated Description", price="12.99")


    response = client.patch(
        f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
        json=updated_dish.model_dump()  # Use model_dump instead of dict
    )
    assert response.status_code == 200
    updated_dish_response = response.json()
    assert updated_dish_response["title"] == updated_dish.title
    assert updated_dish_response["description"] == updated_dish.description
    assert updated_dish_response["price"] == str(updated_dish.price)
    assert updated_dish_response["submenu_id"] == submenu_id

    db_dish = db.query(Dish).filter_by(id=dish_id).first()
    assert db_dish is not None
    assert db_dish.title == updated_dish.title
    assert db_dish.description == updated_dish.description
    assert db_dish.price == updated_dish.price
    assert db_dish.submenu_id == submenu_id

    db.query(Dish).filter(Dish.id == dish_id).delete()
    db.query(Submenu).filter(Submenu.id == submenu_id).delete()
    db.query(Menu).filter(Menu.id == menu_id).delete()
    db.commit()


def create_test_menu_submenu_dish3(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    menu = Menu(id=menu_id, title="Test Menu", description="Test Description")
    db.add(menu)
    db.commit()
    db.refresh(menu)

    submenu = Submenu(id=submenu_id, title="Test Submenu", description="Test Submenu Description", menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)

    dish = Dish(id=dish_id, title="Test Dish", description="Test Description", price="10.99", submenu_id=submenu_id)
    db.add(dish)
    db.commit()
    db.refresh(dish)

    return menu, submenu, dish


def test_delete_dish(client: TestClient, db: Session):
    menu_id = str(uuid4())
    submenu_id = str(uuid4())
    dish_id = str(uuid4())
    menu, submenu, dish = create_test_menu_submenu_dish3(db, menu_id, submenu_id, dish_id)

    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    delete_response = response.json()
    assert delete_response["message"] == "Блюдо удалено"

    db_dish = db.query(Dish).filter_by(id=dish_id).first()
    assert db_dish is None

    db.query(Submenu).filter(Submenu.id == submenu_id).delete()
    db.query(Menu).filter(Menu.id == menu_id).delete()
    db.commit()

import pytest

from models import Menu, Submenu, Dish


@pytest.fixture
def create_menu(client, db):
    response = client.post("/api/v1/menus", json={"title": "Test Menu", "description": "Test Description"})
    assert response.status_code == 201
    created_menu = response.json()
    yield created_menu
    # Удаление меню после теста
    db.query(Menu).filter(Menu.id == created_menu["id"]).delete()
    db.commit()


@pytest.fixture
def create_submenu(client, db, create_menu):
    menu_id = create_menu["id"]
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert response.status_code == 201
    created_submenu = response.json()
    yield created_submenu
    db.query(Submenu).filter(Submenu.id == created_submenu["id"]).delete()
    db.commit()


@pytest.fixture
def create_dish(client, db, create_menu, create_submenu):
    menu_id = create_menu["id"]
    submenu_id = create_submenu["id"]
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json={"title": "Test Dish", "description": "Test Dish Description", "price": "10.99"})
    assert response.status_code == 201
    created_dish = response.json()
    yield created_dish
    db.query(Dish).filter(Dish.id == created_dish["id"]).delete()
    db.commit()


def get_submenus_count(db, menu_id):
    return db.query(Submenu).filter(Submenu.menu_id == menu_id).count()


def get_dishes_count(db, submenu_id):
    return db.query(Dish).filter(Dish.submenu_id == submenu_id).count()



# Тесты
def test_create_menu(create_menu):
    # Тест создания меню
    pass


def test_create_submenu(create_submenu):
    # Тест создания подменю
    pass


def test_create_dish(create_dish):
    # Тест создания блюда
    pass


def test_get_menu(client, create_menu):
    menu_id = create_menu["id"]
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    menu = response.json()
    assert menu["id"] == menu_id


def test_get_submenu(client, create_submenu):
    menu_id = create_submenu["menu_id"]
    submenu_id = create_submenu["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    submenu = response.json()
    assert submenu["id"] == submenu_id


def test_delete_submenu(client, db, create_submenu):
    menu_id = create_submenu["menu_id"]
    submenu_id = create_submenu["id"]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert db.query(Submenu).filter(Submenu.id == submenu_id).first() is None
    assert get_submenus_count(db, menu_id) == 0


def test_list_submenus(client, db, create_menu):
    menu_id = create_menu["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    submenus = response.json()
    assert isinstance(submenus, list)
    assert len(submenus) == get_submenus_count(db, menu_id)


def test_list_dishes(client, db,  create_submenu):
    menu_id = create_submenu["menu_id"]
    submenu_id = create_submenu["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    assert len(dishes) == get_dishes_count(db, submenu_id)


def test_get_dish(client, create_dish, create_menu):
    menu_id = create_menu["id"]
    submenu_id = create_dish["submenu_id"]
    dish_id = create_dish["id"]
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    dish = response.json()
    assert dish["id"] == dish_id


def test_delete_dish(client, db, create_dish, create_menu):
    menu_id = create_menu["id"]
    submenu_id = create_dish["submenu_id"]
    dish_id = create_dish["id"]
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 200
    assert db.query(Dish).filter(Dish.id == dish_id).first() is None
    # Проверка количества блюд после удаления
    assert get_dishes_count(db, submenu_id) == 0


def test_delete_menu(client, db, create_menu):
    menu_id = create_menu["id"]
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert db.query(Menu).filter(Menu.id == menu_id).first() is None
    # Проверка количества подменю после удаления меню
    assert get_submenus_count(db, menu_id) == 0


def test_get_menu_after_deletion(client, create_menu):
    menu_id = create_menu["id"]
    client.delete(f"/api/v1/menus/{menu_id}")
    response = client.get(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 404


def test_get_submenu_after_deletion(client, create_submenu):
    menu_id = create_submenu["menu_id"]
    submenu_id = create_submenu["id"]
    client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 404


def test_get_dish_after_deletion(client, create_dish, create_menu):
    menu_id = create_menu["id"]
    submenu_id = create_dish["submenu_id"]
    dish_id = create_dish["id"]
    client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
    assert response.status_code == 404


def test_list_submenus_after_deletion(client, create_menu):
    menu_id = create_menu["id"]
    client.delete(f"/api/v1/menus/{menu_id}")
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {'detail': 'Меню не найдено'}


def test_list_dishes_after_deletion(client, create_submenu):
    menu_id = create_submenu["menu_id"]
    submenu_id = create_submenu["id"]
    client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    dishes = response.json()
    assert isinstance(dishes, list)
    assert len(dishes) == 0

from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Menu, Submenu, Dish


def get_menus_with_counts(db: Session):
    # Выполняем запрос к базе данных
    menus = db.query(
        Menu.id,
        Menu.title,
        Menu.description,
        func.count(Submenu.id).label('submenus_count'),
        func.count(Dish.id).label('dishes_count')
    ).join(
        Submenu, Menu.id == Submenu.menu_id, isouter=True
    ).join(
        Dish, Submenu.id == Dish.submenu_id, isouter=True
    ).group_by(
        Menu.id
    ).all()

    # Преобразуем результаты запроса в список словарей
    result = []
    for menu in menus:
        result.append({
            'id': str(menu.id),
            'title': menu.title,
            'description': menu.description,
            'submenus_count': menu.submenus_count,
            'dishes_count': menu.dishes_count
        })

    return result

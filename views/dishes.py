from uuid import UUID
from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from core.db import get_db
from sqlalchemy.orm import Session

from models import Menu
from models import Dish
from schemas import DishCreate, DishUpdate

router = APIRouter(tags=["Блюда"])


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
async def get_dishes_list(menu_id: Optional[UUID | str] = None, submenu_id: Optional[UUID | str] = None,
                          db: Session = Depends(get_db)):
    """Получаем блюда по меню и подменю"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    if not my_menu.submenus:
        return []
    my_submenu = None
    for item in my_menu.submenus:
        if str(item.id) == submenu_id:
            my_submenu = item
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    dishes = my_submenu.dishes
    return dishes


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def get_dish(menu_id: Optional[UUID | str] = None, submenu_id: Optional[UUID | str] = None,
                   dish_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Полчучение конкретного блюда"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_submenu = None
    for submenu in my_menu.submenus:
        if str(submenu.id) == submenu_id:
            my_submenu = submenu
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    my_dish = None
    for dish in my_submenu.dishes:
        if str(dish.id) == dish_id:
            my_dish = dish
            break
    if not my_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return my_dish


@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", status_code=201)
async def create_dish(dish: DishCreate, menu_id: Optional[UUID | str] = None,
                      submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Добавление блюда"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_submenu = None
    for submenu in my_menu.submenus:
        if str(submenu.id) == submenu_id:
            my_submenu = submenu
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    dish = Dish(title=dish.title, price=dish.price, submenu_id=submenu_id, description=dish.description)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish


@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def update_dish(dish: DishUpdate, menu_id: Optional[UUID | str] = None, submenu_id: Optional[UUID | str] = None,
                      dish_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Обнавление блюда"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_submenu = None
    for submenu in my_menu.submenus:
        if str(submenu.id) == submenu_id:
            my_submenu = submenu
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    my_dish = None
    for item in my_submenu.dishes:
        if str(item.id) == dish_id:
            my_dish = item
            break
    if not my_dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    my_dish.title = dish.title
    my_dish.id = dish_id
    my_dish.description = dish.description
    my_dish.submenu_id = submenu_id
    my_dish.price = dish.price
    db.commit()
    db.refresh(my_dish)
    return my_dish


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(menu_id: Optional[UUID | str] = None, submenu_id: Optional[UUID | str] = None,
                      dish_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Удаление блюда"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_submenu = None
    for submenu in my_menu.submenus:
        if str(submenu.id) == submenu_id:
            my_submenu = submenu
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    my_dish = None
    for dish in my_submenu.dishes:
        if str(dish.id) == dish_id:
            my_dish = dish
            break
    if not my_dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    db.delete(my_dish)
    db.commit()
    return {"message": "Блюдо удалено"}

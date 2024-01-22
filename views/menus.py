from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.db import get_db
from models import Menu
from schemas import MenuCreate, MenuUpdate

router = APIRouter(tags=["Меню"])


@router.get("/api/v1/menus/{menu_id}")
async def get_menu(menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Получем кокретное меню"""
    if menu_id is not None:
        menu = db.query(Menu).filter_by(id=menu_id).first()
        if menu:
            menu.submenus_count = len(menu.submenus)
            if menu.submenus_count > 0:
                total = 0
                for item in menu.submenus:
                    submenu_dishes_count = len(item.dishes)
                    total += submenu_dishes_count
                menu.dishes_count = total
            return menu
        raise HTTPException(status_code=404, detail="menu not found")
    return None


@router.get("/api/v1/menus")
async def get_menus_list(db: Session = Depends(get_db)):
    """Получаем все меню"""
    menus = db.query(Menu).all()
    if menus:
        return menus
    return []


@router.post("/api/v1/menus", status_code=201)
async def create_menu(
        menu: MenuCreate,
        db: Session = Depends(get_db)):
    """Добавляем новое меню"""
    menu = Menu(title=menu.title, description=menu.description, submenus_count=0, dishes_count=0)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.patch("/api/v1/menus/{menu_id}")
async def update_menu(menu: MenuUpdate, menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Обнавление меню"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_menu.title = menu.title
    my_menu.id = menu_id
    my_menu.description = menu.description
    db.commit()
    db.refresh(my_menu)
    return my_menu


@router.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Удаление меню"""
    menu = db.query(Menu).filter_by(id=menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    db.delete(menu)
    db.commit()
    return {"message": "Меню удалено"}

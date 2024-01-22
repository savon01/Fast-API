from fastapi import APIRouter
from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from core.db import get_db
from models import Menu
from models import Submenu
from schemas import SubmenuCreate, SubmenuUpdate

router = APIRouter(tags=["Подменю"])


@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def get_submenu(menu_id: Optional[UUID | str] = None, submenu_id: Optional[UUID | str] = None,
                      db: Session = Depends(get_db)):
    """Получение конкретного подменю"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_submenu = None
    for submenu in my_menu.submenus:
        if str(submenu.id) == submenu_id:
            my_submenu = submenu
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    my_submenu.dishes_count = len(my_submenu.dishes)
    return my_submenu


@router.get("/api/v1/menus/{menu_id}/submenus")
async def get_submenus_list(menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Получаем подменю все"""
    menu = db.query(Menu).filter_by(id=menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    submenus = menu.submenus
    return submenus


@router.post("/api/v1/menus/{menu_id}/submenus", status_code=201)
async def create_submenu(submenu: SubmenuCreate, menu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Добовляем подменю"""
    existing_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not existing_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    submenu = Submenu(title=submenu.title, description=submenu.description, menu_id=menu_id)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu


@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def update_submenu(submenu: SubmenuUpdate, menu_id: Optional[UUID | str] = None,
                         submenu_id: Optional[UUID | str] = None, db: Session = Depends(get_db)):
    """Обнавляем данные меню"""
    my_menu = db.query(Menu).filter_by(id=menu_id).first()
    if not my_menu:
        raise HTTPException(status_code=404, detail="Меню не найдено")
    my_submenu = None
    for item in my_menu.submenus:
        if str(item.id) == submenu_id:
            my_submenu = item
            break
    if not my_submenu:
        raise HTTPException(status_code=404, detail="Подменю не найдено")
    my_submenu.title = submenu.title
    my_submenu.description = submenu.description
    db.commit()
    db.refresh(my_submenu)
    return my_submenu


@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(menu_id: Optional[UUID | str] = None, submenu_id: Optional[UUID | str] = None,
                         db: Session = Depends(get_db)):
    """Удаляет меню"""
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
    db.delete(my_submenu)
    db.commit()
    return {"message": "Меню удалено"}

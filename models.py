import uuid

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core.db import Base


class Menu(Base):
    """Модель меню"""
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete')
    submenus_count = Column(Integer)
    dishes_count = Column(Integer)


class Submenu(Base):
    """Модель для подменю"""
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    menu_id = Column(UUID, ForeignKey('menus.id'))
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete')
    dishes_count = Column(Integer)


class Dish(Base):
    """Модель для блюда"""
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(UUID, ForeignKey('submenus.id'))
    submenu = relationship('Submenu', back_populates='dishes')

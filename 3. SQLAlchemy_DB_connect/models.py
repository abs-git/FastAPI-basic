import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    # talbe 생성
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(80), unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates='owner')

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    onwer_id = Column(Integer, ForeignKey('users.id'))

    onwer = relationship("User", back_populaties='items')

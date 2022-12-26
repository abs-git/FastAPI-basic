# Session 모듈이 db라는 파라미터를 생성하고 데이터베이스와 소통하도록 한다.

from sqlalchemy.orm import Session
from . import models, schemas

# READ
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# CREATE
def create_user(db: Session, user: schemas.UserCreate):
    # sqlalchemy 객체 생성 -> add()를 이용해 데이터베이스에 추가 
    # -> commit()를 이용해 데이터베이스에 반영 -> refresh()로 데이터베이스 갱신

    fake_hashed_password = user.password + "extra"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh()
    return db_item


# UPDATE
def update_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.email = "updated@email"
    db.add(user)
    db.commit()
    return user


# DELETE
def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit
    return 'user_id : {} delete'.format(user_id)
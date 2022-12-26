# pydantic 모델은 api의 데이터를 읽고 리턴할 때 사용하는 모델이다.
# 즉, pydantic으로 데이터를 읽고, 읽은 데이터를 이용해 sqlalchemy의 객체를 생성하고 db에 넣어준다.
# 이를 다시 리턴하기 위해선 pydantic을 사용한다.

from typing import List, Optional
from pydantic import BaseModel

# Item scheme
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    class Config:
        # orm_mode가 true이면 dict 타입이 아니여도 값을 읽을 수 있게 해준다.
        # 이는, sqlalchemy를 리턴할 때, pydantic 모델로의 변환 과정에서 데이터에 접근하게 되고
        # 릴레이션 데이터를 불러와서 같이 리턴한다.
        orm_mode=True

# User scheme
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode=True

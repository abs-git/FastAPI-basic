from typing import List, Optional
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

app = FastAPI()


#### response model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float]=None
    tags: List[str] = []

@app.post('/items/', response_model=Item)
async def create_item(item: Item):
    # output을 response_model에서 지정한 모델로 변환
    # response에 json 스키마 추가
    # doc 시스템 이용
    return item

## 예시
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str]=None

@app.post('/users/', response_model=UserOut)
async def create_user(user: UserIn):
    # 입력으로 UserIn이 들어오고 
    # 출력으로 UserOut이 반환된다.
    return user


## include, exclude
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},

)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]



# Multiple models
# 여러 모델에서 중복된 내용을 제거하기 위해 상속을 활용한다. 
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

def fake_password_hasher(raw_password: str):
    return 'secret' + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    return user_in_db

@app.post('/user/', response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved



#### response status code
# 100~ : information, 사용할 일 없음, response body를 가질 수 없다.
# 200~ : 요청에 대한 처리가 성공.
# 300~ : Redirection 을 의미.
# 400~ : Client error
# 500~ : Server error

@app.post('/items/', status_code=201)
async def create_item(name: str):
    return {'name': name}


@app.post('/items/', status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {'name': name}


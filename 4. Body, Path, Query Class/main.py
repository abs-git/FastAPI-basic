# Query, Path, Body class 활용
# Request body 내의 metadata를 Feild class로 제어

from typing import Optional, List
from fastapi import FastAPI
from fastapi import Query, Path, Body
from pydantic import BaseModel, Field, HttpUrl

class Item(BaseModel):
    # Request body 라고한다.
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()

@app.post('/items/')
async def create_item(item: Item):
    # 모델 attribute에 직접 접근 혹은 dict으로 받아올 수 있다.
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({'price_with_tax': price_with_tax})
    return item_dict


@app.put('/items/{item_id}')
async def create_item(item_id:int, item: Item, q: Optional[str]=None):
    # request body, path parameter, query parameter가 전부 존재
    result = {'item_id': item_id, **item.dict()}
    if q:
        result.update({'q':q})
    return result



### Query parameter 예제
@app.get('/items/')
async def read_items(q: Optional[str] = Query(None, min_length=5, max_length=50)):
    # Query(None, max_length=50) : 기본 값은 None, 최소 길이 5, 최대 길이 50
    # regex='^fixedquery$', title, descriptiona 등의 파라미터로 쿼리 설정
    # Query(..., min_length=5) : 기본 값으로 초기화 된다.
    results = {'items': [{'item_id': 'Foo'}, {'item_id': 'Bar'}]}
    if q:
        results.update({'q':q})
    return results

q = Optional[str] = Query(None, alias='item-query')
async def read_items(q: Optional[str]=Query(None, alias='item-query')):
    # alias parameter 예시
    return q



### Path Parameter 예제
@app.get('items/{item_id}')
async def read_items(*, item_id: int = Path(..., title='item id'), q: Optional[str]=None):
    # Path(..., gt=0, le=100, ge=0, lt=10) : 숫자의 길이 범위 지정
    return item_id, q


### Body class
@app.put('/items/{item_id}')
async def update_item(
    item_id: int, item: Item, importance: int= Body(..., embed=True)
):
    results = {'item_id': item_id, 'item': item, 'importance': importance}
    return results



### Field 예제
class Image(BaseModel):
    url: HttpUrl
    url: str
    name: str

class User(BaseModel):
    name: str
    description: Optional[str] = Field(None, title='description', max_length=300)
    age: int = Field(..., gt=0, description='age')
    tags: List[str] = []

    image: Optional[Image] = None   # 하나의 모델은 다른 모델 안에서 사용가능


@app.put('/users/{user_id}')
async def update_user(user_id: int, user: User = Body(..., embed=True)):
    results = {'user_id': user_id, 'user': user}




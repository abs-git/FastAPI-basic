# jsonable_encoder는 데이터 타입을 json과 호환되도록 변형한다.

from typing import Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

app = FastAPI()

items = {
    'dong': {'name': 'dong', 'price': 50.2},
    'hyun': {'name': 'hyun', 'price': 45.2, 'description': 'example'}
}

class Item(BaseModel):
    title: str
    price: Optional[float] = None
    description: Optional[str] = None

@app.get('/items/{item_id}', response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

@app.patch('/items/{item_id}', response_model=Item)
def update_item(item_id: str, item: Item):
    item_data = items[item_id]
    item_model = Item(**item_data)

    update_data = item.dict(exclude_unset=True)
    update_item = item_model.copy(update=update_data)

    items[item_id] = jsonable_encoder(update_item)

    return update_item

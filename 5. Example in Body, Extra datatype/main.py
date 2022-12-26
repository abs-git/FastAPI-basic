# Path(), Query(), Header(), Cookie(), Body(), Form(), File() 에서 example 혹은 examples를 사용할 수 있다.
# date, time, uuid 등의 data type을 사용할 수도 있다.

from typing import Optional
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

from datetime import datetime, time, timedelta
from uuid import UUID


app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str]=None
    price: float
    tax: Optional[float]=None

    class Config:
        schema_extra = {
            "example": {
                'name': 'donghyun',
                'description': 'item example',
                'price': 4.5,
                'tax': 0.45
            }
        }

class Item2(BaseModel):
    name: str = Field(..., example = 'donghyun')
    description: Optional[str]= Field(None, example='item2 example')
    price: float = Field(..., example=4.5)
    tax: Optional[float]= Field(..., example=0.45)


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    results = {'item_id': item_id, 'item': item}
    return results


@app.put('/items/{item_id}')
async def update_item(
    *, 
    item_id: int, 
    item: Item = Body(
        ...,
        examples={
            'example 1':{},
            'example 2':{},
            'example 3':{}
            }
        )
    ):

    results = {'item_id': item_id, 'item': item}
    return results



### Extra data type
@app.put('/items/{item_id}')
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime]= Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after = Optional[timedelta] = Body(None)
    )

    return {'item_id': item_id, }

import uvicorn
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class EnumBye(str, Enum):
    # 미리 정해진 값으로 객체를 생성하고 싶으면 enum을 권장한다.
    name = 'dong'
    email = 'hyun'
    address = 'kang'


class Bye(BaseModel):      
    # fastapi에서 request body를 만들기 위해선 pydantic models를 이용한다.
    # type hint : 파라미터 값이 어떤 자료형으로 들어와야 하는지 명시.
    name:str
    id:int
    description:Optional[str] = None


@app.get('/')
def root():
    root = 'This is root page'
    return root


@app.get("/hi")               # 기본 get 페이지
async def get_hi():
    hi = 'hi'
    return hi

@app.post("/bye")
async def post_bye(bye: Bye):
    # attribute에 직접 접근하거나 dict으로 받아와 데이터를 업데이트 할 수 있다.
    bye_info = bye.dict()
    if bye.description:
        bye_info.update({'description':bye.description})
    return bye



@app.get("/items/{item_id}")
def get_item(item_id:int, query:Optional[str]=None):        # optional parameter
    # path parameter라고 하며, path를 등록할 때 순서에 유의해야한다.
    # /items/0?query=q
    if query: 
        return {"item_id":item_id, "query":query}
    return {'item_id':item_id}




@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


if __name__ == '__main__':
    uvicorn.run(app, port=8080)     #>> uvicorn main:app --reload --host=0.0.0.0 --port=8080 과 동일하다.

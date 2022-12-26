import uvicorn
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, Query

app = FastAPI()

class Bye(BaseModel):
    name:str
    id:int
    description:Optional[str] = None


@app.get('/')
def root():
    root = 'This is root page'
    return root


@app.get("/items/")
async def get_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="regurations_str")):
    results = {'items': [{'item_id':'dong', 'item_id':'hyun'}]}
    if q:
        results.update({'q':q})
    return results

@app.get("/items2/")
async def get_items2(q: Optional[List[str]] = Query(None)):
    # http://localhost:8000/items/?q=foo&q=bar 
    # List를 이용하면 위와 같이 여러개의 요청 값을 줄 수 있다.
    query_items = {'q':q}
    return query_items



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

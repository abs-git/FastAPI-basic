import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from dependencies import get_query_token, get_token_header
from routers import items, users
from common_router import common

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(users.router)        # 라우터를 main app에 추가
app.include_router(items.router)
app.include_router(
    common.router,
    prefix="/common",
    tags=["common"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "custom router"}},
)

class Item(BaseModel):
    name:str
    number:int

@app.get('/')
async def root():
    root = 'This is root page'
    return root

@app.get("/hi")
async def get_hi():
    hi = 'hi'
    return hi

@app.post("/bye")
async def post_bye(item:Item):
    return item


if __name__ == '__main__':
    uvicorn.run(app, port=8080)     #>> uvicorn main:app --reload --host=0.0.0.0 --port=8080 과 동일하다.

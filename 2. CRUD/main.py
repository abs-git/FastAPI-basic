# GET, POST, DELETE, PATCH (update) 예제
import uvicorn
import uuid
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI
from starlette.responses import JSONResponse, Response


app = FastAPI()


@app.route('/state')
async def state_check():
    return "OK"


# get 메소드는 서버로부터 리소스를 읽을 때 사용 (READ)
@app.get('/{name}', description='name을 받아 ID를 생성한다.')
async def read_user_id(name:str):
    # JSONResponese를 활용하여, dict 을 json으로 변형한다. 
    return JSONResponse({
        'id': str(uuid.uuid4()),
        'name':name
    })


# 서버에 데이터를 저장할 때 사용하는 객체 클래스이다. (CREAT)
class Item(BaseModel):
    # FastAPI에서 poser를 할 땐 스키마 디펜던시가 있다.
    # FastAPI에서는 기본적으로 pydantic을 사용하기 때문에 pydntic.BaseModel을 상속해야만 한다. 
    user_id: str = Field(title = '사용자의 id')
    password: str = Field(title = '사용자의 password')

class PacthItem(BaseModel):
    # pacth를 위해선 optional 타입인 멤버 변수들이 필요하다.
    # optinal을 붙여줌으로써 pydantic이 멤버 중 입력되지 않는 경우라도 실행될 수 있도록 한다. 
    user_id: Optional[str]
    password: Optional[str]


class ResponseItem(Item):
    # 응답 모델에 대한 클래스
    success: bool

# post는 객체를 생성할 때 사용한다.
@app.post('/resigter', response_model=ResponseItem)
async def register_item(item: Item):
    item_dict = dict(item)
    item_dict['success'] = True
    return JSONResponse(item_dict)


# put은 모든 내용을 바꾸는 용도로 사용된다. (UPDATE)
@app.put('/update')
async def update_item(item:Item):
    item_dict = {k:v for k,v in dict(item).items()}
    item_dict['success']=True
    return JSONResponse


# patch는 일부 내용을 바꾸는 용도로 사용된다. (UPDATE)
@app.patch('/update')
async def update_item_parts(item:PacthItem):
    item_dict = {}
    for k, v in dict(item).items():
        if v:
            item_dict[k] = v
    item_dict['success']=True
    return JSONResponse(item_dict)


# delete은 객체를 삭제한다. (DELETE)
@app.delete('/delete')
async def delete_item():
    item_dict = None
    return Response(status_code=204)



if __name__ == '__main__':
    uvicorn.run(app, port=8080)     #>> uvicorn main:app --reload --host=0.0.0.0 --port=8080 과 동일하다.

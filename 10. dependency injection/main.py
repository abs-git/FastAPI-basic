# Dependency Injection이란 중복 코드 제거를 위한 코드 재활용 기법이다. 
# Depends 클래스를 활용하며 Class dependency, Sub dependency, Dependency in Decorator, Global dependency
# 등으로 활용한다.

from typing import Optional

from fastapi import Depends, FastAPI, Cookie
from fastapi import Header, HTTPException

app = FastAPI()


### 일반적인 예시
# dependency가 걸린 함수는 데코레이터(@) 없는 path operation과 유사하다.
async def common_parameters(q: Optional[str]=None, skip: int=0, limit: int=100):
    return {'q': q, 'skip': skip, 'limit': limit}


@app.get('/items/')
async def read_items(commons: dict= Depends(common_parameters)):
    return commons

@app.get('/users/')
async def read_users(commons: dict= Depends(common_parameters)):
    return commons


### Class dependency
fake_items_db = [{'item_name': 'dong'},
                 {'item_name': 'hyun'},
                 {'item_name': 'kang'}
                ]

class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int=0, limit: int=100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get('/items/')
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({'q': commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({'items': items})
    return response


### Sub dependency
# dependency in dependency
def query_extractor(q: Optional[str] = None):
    # 디펜던시의 디펜던시
    return q

def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)):
    # 디펜던시
    if not q:
        return last_query
    return q

@app.get('/items/')
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    # path operation 연결
    return {'q_or_cookie': query_or_default}



### Dependency in Decorator
# 디펜던시가 리턴값 없이 실행이 필요한 경우 사용
async def verify_token(token: str = Header(...)):
    if token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail='Token header invalid')

async def verify_key(key: str = Header(...)):
    # 값을 리턴하지만, path operation에 전달되지 않는다.
    if key != 'fake-super-secret-key':
        raise HTTPException(status_code=400, detail='Key header invalid')
    return key

@app.get('/items/', dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{'item': 'dong'}, {'item': 'hyun'}]


### Global dependency
# app = FastAPI(dependencies = [Depends(verify_token), Depends(verify_key)])


### Dependency with yield
# 디펜던시 후 작업 수행
async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()



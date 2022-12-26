# 간단한 라우터 예제
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=['users'])
async def read_users():
    return [{'username':"dong"},
            {'username':'kang'}]


@router.get("/users/me", tags=['users'])
async def read_user_me():
    return {'username': 'donghyun'}


@router.get('/users/{username}', tags=['users'])
async def read_user(username: str):
    return {'username':username}



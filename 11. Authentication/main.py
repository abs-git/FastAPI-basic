# OAuth2 : 인증, 권한부여에 대한 시스템 ex) 소셜 로그인
# OpenID Connect : OAuth2 기반 인증 시스템.
# flow : OAuth2의 security를 다루는 행위

from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel


# password flow
'''
1) user가 Front-end에서 id와 pw를 입력한다.
2) Front-end는 id과 pw를 APU의 URL에 전송한다. (tokenUrl = )
3) API는 response로 token을 반환한다. (유저 확인용)
    token은 front-end에 저장되며, 유통기한이 있다.
4) 로그인 후 Back-end에 데이터를 요청할 시, authentication이 필요한 경우
    front-end에선 헤더에 Bearer + token 값을 보낸다.
    Bearer +token이 아닐 시 401 에러가 발생한다.
'''

app = FastAPI()


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def fake_hash_password(password: str):
    return 'fakehashed' + password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='toke')       # callable한 객체이므로 Depends가 가능하다.

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[str] = None

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='example',
            headers={'WWW-Athenticate': 'Bearer'}
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='example')
    return current_user



@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="example")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="example")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

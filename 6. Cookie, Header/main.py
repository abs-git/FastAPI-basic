from typing import Optional
from fastapi import FastAPI, Cookie, Header

app = FastAPI()

@app.get('/items/')
async def read_items(item_id: Optional[str] = Cookie(None)):
    return {'item_id': item_id}

@app.get('/users/')
async def read_users(user_id: Optional[str] = Header(None)):
    return {'user_id': user_id}




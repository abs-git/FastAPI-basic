# CORS (Cross Origin Resource Sharing) : 프론트엔드와 백엔드간 Origin이 다를 때 생기는 상황
# Origin : protocol(http, https) + domain(.com, localhost) + port(8080)

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


### 미들웨어 예제
@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time

    response.headers['process-time'] = str(process_time)
    return response


### CORS 미들웨어 예제
origins = [
    'http://localhost.com',
    'https://localhost.com',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials =True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def main_page():
    return {'message': 'hello world'}




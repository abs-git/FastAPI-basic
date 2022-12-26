# 간단한 라우터 예제
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header

router = APIRouter(
    prefix='/common',
    tags=['common'],
    dependencies=[Depends(get_token_header)],
    responses={404: {'description':'Not found'}}
)

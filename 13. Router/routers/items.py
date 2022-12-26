from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_token_header

router = APIRouter(
    prefix='/items',
    tags=['items'],
    dependencies=[Depends(get_token_header)],
    responses={404: {'description':'Not found'}}
)

fake_items_db = {'dong': {'name':'dong'},
                 'hyun': {'name':'hyun'}
}

@router.get('/')
async def read_items():
    return fake_items_db

@router.get('/{item_id}')
async def read_item(item_id:str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail='item not found')
    return {'name':fake_items_db[item_id]['name'], 'item_id':item_id}

@router.put('/{item_id}', tags=['custom'], responses={403: {'description': 'operation forbidden'}})
async def update_item(item_id: str):
    if item_id != 'dong':
        raise HTTPException(status_code=403, detail='you can only update the item: dong')
    return {'item_id': item_id, 'name':'dong'}


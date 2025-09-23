from fastapi import HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from app.core.utils import read_json

api_key_header = APIKeyHeader(name='Authorization')

async def get_current_user(token: str = Depends(api_key_header)):
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized user!')

    users = await read_json('users.json')

    for user in users:
        if user.get('token') == token:
            return user
    raise HTTPException(status_code=400, detail='Invalid token!')

def required_role(role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if role == user['role']:
            return user
        raise HTTPException(status_code=403, detail='Insufficient role')

    return role_checker

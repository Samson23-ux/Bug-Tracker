from fastapi import APIRouter, HTTPException, Form
from app.schemas.users import AccountCreate, AccountUpdate, Response
from app.services.users import user_service

router = APIRouter()

@router.post('/sign-up/', status_code=201, response_model=Response)
async def create_account(account: AccountCreate):
    user_acc = await user_service.create_user(account.model_dump())
    user_acc = user_service.remove_password(user=user_acc)

    return Response(message='Account created successfully!', data=user_acc)

@router.post('/sign-in/{user_id}/', status_code=201, response_model=Response)
async def sign_user_in(user_id: str, username: str = Form(...), password: str = Form(...)):
    user_acc = await user_service.sign_user_in(user_id, username, password)
    user_acc = user_service.remove_password(user=user_acc)

    return Response(message='Sign in successful!', data=user_acc)

@router.patch('/sign-out/{user_id}/', response_model=Response)
async def sign_user_out(user_id: str):
    user_acc = await user_service.sign_user_out(user_id)
    user_acc = user_service.remove_password(user=user_acc)

    return Response(message='Sign out successful!', data=user_acc)

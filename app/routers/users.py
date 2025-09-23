from fastapi import APIRouter, Depends, Query, Form
from typing import Optional
from app.schemas.users import AccountUpdate, Response
from app.services.users import user_service
from app.dependencies import get_current_user

router = APIRouter()

@router.get('/', response_model=Response)
async def get_users(
    role: Optional[str] = Query(None, description='Filter by role')
):
    users = await user_service.get_users(role)
    users = user_service.remove_password(users=users)

    return Response(message='Users retrieved successfully!', data=users)

@router.get('/{username}/', response_model=Response)
async def get_user(username: str):
    user = await user_service.get_user(username)
    user = user_service.remove_password(user=user)

    return Response(message='User retrieved successfully!', data=user)

@router.patch('/{user_id}/', response_model=Response)
async def update_account(
    account_update: AccountUpdate,
    user_id: str,
    _ = Depends(get_current_user)
):
    user = await user_service.update_account(user_id, account_update.model_dump(exclude_unset=True),
                                             account_update.password)
    user = user_service.remove_password(user=user)

    return Response(message='Account updated successfully!', data=user)

@router.delete('/{user_id}/', status_code=204)
async def delete_account(
    user_id: str,
    _ = Depends(get_current_user)):
    await user_service.delete_account(user_id)

    return Response(message='Account deleted successfully!')

from typing import Optional
from fastapi import APIRouter, Query, Depends
from app.schemas.bugs import BugCreate, BugUpdate, Response
from app.services.bugs import bug_service
from app.dependencies import get_current_user, required_role

router = APIRouter()

@router.get('/', response_model=Response)
async def get_bugs(
    status: Optional[str] = Query(None, description='Filter by status'),
    severity: Optional[str] = Query(None, description='Filter by severity'),
    assignee: Optional[str] = Query(None, description='Filter by assignee'),
    _ = Depends(get_current_user)
):
    bugs = await bug_service.get_bugs(status, severity, assignee)

    return Response(message='Bugs retrieved successfully!', data=bugs)

@router.get('/user/', response_model=Response)
async def get_reported_bugs(user: dict = Depends(get_current_user)):
    bugs = await bug_service.get_reported_bugs(user['username'])

    return Response(message='Bugs retrieved successfully!', data=bugs)

@router.get('/developer/', response_model=Response)
async def get_assigned_bugs(user: dict = Depends(get_current_user)):
    bugs = await bug_service.get_assigned_bugs(user['username'])

    return Response(message='Bugs retrieved successfully!', data=bugs)

@router.get('/{title}/', response_model=Response)
async def get_bug(title: str, _ = Depends(get_current_user)):
    bug = await bug_service.get_bug(title)

    return Response(message='Bugs retrieved successfully!', data=bug)

@router.post('/', status_code=201, response_model=Response)
async def create_bug(
    bug_create: BugCreate,
    user: str = Depends(get_current_user)
):
    bug = await bug_service.report_bug(bug_create.model_dump(), user['username'])

    return Response(message='Bug reported successfully!', data=bug)

@router.patch('/{bug_id}/assign/', response_model=Response)
async def assign_bug(
    bug_update: BugUpdate,
    bug_id: str,
    user = Depends(get_current_user),
    _ = Depends(required_role('admin'))
):
    bug = await bug_service.update_bug(bug_id, bug_update.model_dump(exclude_unset=True))

    return Response(message='Bug assigned successfully!', data=bug)

@router.patch('/{bug_id}/', response_model=Response)
async def update_bug(
    bug_update: BugUpdate,
    bug_id: str,
    _ = Depends(get_current_user)
):
    bug = await bug_service.update_bug(bug_id, bug_update.model_dump(exclude_unset=True))

    return Response(message='Bug updated successfully!', data=bug)

@router.patch('/{bug_id}/status/', response_model=Response)
async def update_bug_status(
    bug_update: BugUpdate,
    bug_id: str,
    user = Depends(get_current_user),
    _ = Depends(required_role('developer'))
):
    bug = await bug_service.update_bug(bug_id, bug_update.model_dump(exclude_unset=True))

    return Response(message='Bug updated successfully!', data=bug)

@router.delete('/{bug_id}/', status_code=204)
async def delete_bug(bug_id: str, _ = Depends(get_current_user)):
    await bug_service.delete_bug(bug_id)

    return Response(message='Bug deleted successfully!')

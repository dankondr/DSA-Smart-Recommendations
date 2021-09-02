from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException
from starlette import status

from api.auth import (
    EmailPasswordRequestForm,
    Token,
    create_access_token,
    get_current_active_user,
)
from clients import miem_client
from core.settings import settings
from models.user import User
from project.schemas.project import Project, ProjectDetail
from project.schemas.token import Email
from recommendations import get_recommendations

endpoints = APIRouter()


class UserForm:
    def __init__(self, email: Email = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password


@endpoints.post('/register')
async def register(form_data: UserForm = Depends()):
    user = User(email=form_data.email)
    user.password = form_data.password

    await User.manager.create(
        User, email=user.email, password_hashed=user.password_hashed
    )
    return {'message': f'successfully created user with email {user.email}'}


@endpoints.post('/token', response_model=Token)
async def login_for_access_token(form_data: EmailPasswordRequestForm = Depends()):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect email or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    user: User = await User.manager.get(User, email=form_data.email)
    if not user:
        raise exc
    if user.password != form_data.password:
        raise exc
    access_token_expires = timedelta(hours=settings.access_token_expire_hours)
    access_token = create_access_token(
        data={'sub': user.email}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@endpoints.get('/projects', response_model=list[Project])
async def project_all() -> list[Project]:
    projects = await miem_client.get_projects()
    return projects


@endpoints.get('/projects/{project_id}', response_model=ProjectDetail)
async def project(project_id: int) -> ProjectDetail:
    project_detail = await miem_client.get_project(project_id)
    return project_detail


@endpoints.get('/projects/like/{project_id}')
async def like_project(
    project_id: int, current_user: User = Depends(get_current_active_user)
) -> dict:
    await current_user.like(project_id)
    return {'message': f'successfully liked {project_id}'}


@endpoints.get('/projects/recommendations', response_model=list[Project])
async def projects_recommendations(
    current_user: User = Depends(get_current_active_user),
) -> list[Project]:
    recs = await get_recommendations(current_user)
    return recs

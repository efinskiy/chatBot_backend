from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, Security
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from api.auth.schemas import AuthSchema, AuthResponse, BadUsernamePassword, UserCreate, UserRegistrationResponse, \
    UserExists
from api.users.models import User, UserToRole, UserRole, UserRoleToPermission
from database import get_async_session
from .utils import verify_password, check_permissions
from .utils import get_password_hash
from fastapi_jwt import JwtAccessBearer
from fastapi_jwt import JwtAuthorizationCredentials

from ..users.schemas import UserReadSchema

router = APIRouter(prefix='/auth')

access_security = JwtAccessBearer(secret_key="secret_key", auto_error=True)


@router.post('/login', response_model=AuthResponse,
             responses={401: {'model': BadUsernamePassword,
                              'description': 'Bad username or password'}})
async def login(user_data: AuthSchema,
                session: AsyncSession = Depends(get_async_session)):

    user: User = await session.scalar(select(User).where(User.login == user_data.login))

    if not user:
        raise HTTPException(status_code=401, detail="Bad username or password")

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = access_security.create_access_token(subject={'id': user.id},
                                                       expires_delta=timedelta(days=1))
    refresh_token = access_security.create_refresh_token(subject={'id': user.id},
                                                         expires_delta=timedelta(days=7))

    return {"access_token": access_token,
            "refresh_token": refresh_token}


@router.post('/register', response_model=UserRegistrationResponse,
             responses={400: {'model': UserExists,
                              'description': 'User with sended login already registered'}})
async def register(user_data: UserCreate,
                   session: AsyncSession = Depends(get_async_session)):

    if await session.scalar(select(User).where(User.login == user_data.login)):
        raise HTTPException(status_code=400, detail='User already exists')

    new_user = User()
    new_user.login = user_data.login
    new_user.name = user_data.name
    new_user.lastname = user_data.lastname
    new_user.hashed_password = get_password_hash(user_data.password)

    session.add(new_user)
    await session.commit()
    return UserRegistrationResponse


@router.get('/me', response_model=UserReadSchema)
async def me(session: AsyncSession = Depends(get_async_session),
             cred: JwtAuthorizationCredentials = Security(access_security)):
    # user: User = await session.scalar(
    #     select(User)
    #     .where(User.id == cred['id'])
    #     .options(
    #         joinedload(User.roles, innerjoin=True)
    #         .subqueryload(UserToRole.role)
    #         .subqueryload(UserRole.linked_permissions)
    #         .subqueryload(UserRoleToPermission.permission)
    #     )
    # )
    user: User | None = await session.get(User, cred['id'])

    return user


from typing import Union

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from api.users.models import User, UserRole, UserToRole, UserRolePermission, UserRoleToPermission

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def check_permissions(permissions: list, session: AsyncSession, current_user_id: int) -> None:
    user: User | None = await session.scalar(
        select(User)
        .where(User.id == current_user_id)
        .options(
            joinedload(User.roles, innerjoin=True)
            .subqueryload(UserToRole.role)
            .subqueryload(UserRole.linked_permissions)
            .subqueryload(UserRoleToPermission.permission)
        )
    )
    permission_list = []
    for usertorole in user.roles:
        for permission in usertorole.role.linked_permissions:
            permission_list.append(permission.permission.value)
    if 'admin.all' in permission_list: return None

    missed_permissions = []
    for p in permissions:
        if p not in permission_list:
            missed_permissions.append(p)
    if missed_permissions:
        raise HTTPException(status_code=403, detail={'missed_permissions': missed_permissions})





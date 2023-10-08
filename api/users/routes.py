from fastapi import APIRouter
from .models import User, UserToRole, UserRole, UserRoleToPermission, UserRolePermission
router = APIRouter(prefix='/user')


# @router.get('/')
# async def get(sessiom):
#     SessionLocal.


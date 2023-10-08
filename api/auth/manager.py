from typing import Optional, Union
from fastapi_users import IntegerIDMixin, BaseUserManager, schemas, models
from fastapi import Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.models import User, get_user_db
from fastapi_users import exceptions
from api.users.schemas import UserCreate
from database import get_async_session, async_session_maker

SECRET = 'asiudbniuasbduiabiubada'


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)
        session = async_session_maker()
        existing_user = await session.scalar(select(User).where(User.login == user_create.login))

        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)

        # await self.on_after_register(created_user, request)
        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

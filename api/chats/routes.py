from collections.abc import Sequence
from typing import List

from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, label
from sqlalchemy.orm import selectinload, joinedload

from api.auth.routes import access_security
from api.auth.utils import check_permissions
from api.communication.models import ChatUser, Message
from api.communication.schemas import ChatUser as ChatUserSchema
from .schemas import ChatUserWithUnseen, ChatUserWithUserSourceSchema
from database import get_async_session

router = APIRouter(prefix='/chats')


@router.get('', response_model=List[ChatUserWithUserSourceSchema])
async def get_chats(session: AsyncSession = Depends(get_async_session),
                    current_user: JwtAuthorizationCredentials = Security(access_security)):
    await check_permissions(['chat.get'], session, current_user['id'])

    # unseen_messages = await session.scalar(
    #     select(
    #         ChatUser.id,
    #         func.count(ChatUser.messages)
    #     )
    #     .where(Message.message_seen == False)
    #     .group_by(ChatUser.id)
    # )
    unseen_messages = select(func.count(Message.id)).where(Message.message_seen == False).scalar_subquery()

    chat_users: Sequence[ChatUser] = (await session.scalars(
        select(ChatUser, unseen_messages.label('unseen'))
        .where(ChatUser.banned == False)
        .options(
            selectinload(ChatUser.user_source),
            selectinload(ChatUser.messages)
        )
    )).all()

    return chat_users


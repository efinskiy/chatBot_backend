from collections.abc import Sequence
from typing import List

from fastapi import APIRouter, Depends, Security
from pydantic import Field
from sqlalchemy import select, ScalarResult, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from api.communication.models import Message, ChatUser
from api.communication.schemas import MessageSchema, MessageCreate, GetByUserId
from bots.telegram.bot import bot
from fastapi_jwt import JwtAuthorizationCredentials
from ..auth.routes import access_security
from ..auth.utils import check_permissions

router = APIRouter(prefix='/messages')

from database import get_async_session


@router.get('/', response_model=List[MessageSchema])
async def get(session: AsyncSession = Depends(get_async_session)):
    messages = await session.scalars(
                                    select(Message)
                                    .limit(10)
                                    .options(
                                        joinedload(Message.user),
                                        joinedload(Message.reply_user)
                                    )
    )
    result = messages.all()

    print(result)
    return result


@router.get('/by_user', response_model=List[MessageSchema])
async def get_by_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    messages: Sequence[Message] = (await session.scalars(
        select(Message)
        .where(Message.user_id == user_id)
        .options(
            joinedload(Message.user)
        )
    )).all()
    for m in messages:
        m.message_seen = True
        session.add(m)
    await session.commit()
    return messages


@router.post('/')
async def send(message: MessageCreate, session: AsyncSession = Depends(get_async_session),
               current_user: JwtAuthorizationCredentials = Security(access_security)):
    await check_permissions(['chat.message.send'], session, current_user['id'])

    await bot.send_message(message.chat_id, message.text)

    new_message: Message = Message(**message.model_dump())
    new_message.reply_user_id = current_user['id']
    chatuser: ChatUser | None = await session.scalar(select(ChatUser).where(ChatUser.platform_id == message.chat_id))
    new_message.user_id = chatuser.id
    new_message.is_reply = True

    session.add(new_message)
    await session.commit()

    return {'status': 'Message send'}


@router.get('/unseen')
async def get_unseen(user_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: JwtAuthorizationCredentials = Security(access_security)):
    await check_permissions(['chat.get'], session, current_user['id'])
    unseen = await session.scalar(
        select(func.count(Message.id))
        .where(and_(
            Message.message_seen == False,
            Message.user_id == user_id
        ))
    )

    return {'unseen': unseen}


@router.delete('/')
async def delete_all(session: AsyncSession = Depends(get_async_session)):
    messages = (await session.scalars(select(Message))).all()
    for m in messages: await session.delete(m)
    await session.commit()
    return {'message': f'Deleted {len(messages)} messages'}

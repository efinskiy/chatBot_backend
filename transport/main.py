from aiohttp import web

import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from api.communication.models import ChatUser, Message
from api.communication.schemas import MessageCreate

from database import get_async_session

sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ, auth):
    print(f'connected auth={auth} sid={sid}')
    await sio.emit('hello', (1, 2, {'hello': 'you'}), to=sid)


@sio.event
async def disconnect(sid):
    print('disconnected', sid)


@sio.event
async def new_message(sid, data):
    print(f'Event: new_message, sID: {sid}')

    await sio.emit('new_message',
                   data=data,
                   skip_sid=sid)


@sio.event
async def reply_message(sid, data):
    print(data, sid)
    await sio.emit('reply_message', data=data, skip_sid=sid)

if __name__ == '__main__':
    web.run_app(app, port=5000)
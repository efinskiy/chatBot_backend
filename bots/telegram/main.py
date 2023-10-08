import socketio
from socketio import AsyncClient
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from bot import bot
from telebot.types import Message

from api.communication.models import Message as DBMessage, UserSource, AttachmentTypes
from api.communication.models import ChatUser

from database import async_session_maker, get_async_session

sio = socketio.AsyncClient()


@sio.event
async def new_message(sid, auth):
    print(sid)


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
async def reply_message(data: dict):
    await bot.send_message(
        chat_id=data['chat_id'],
        text=data['message'],
        reply_to_message_id=data['reply_to'] if data['reply_to'] else None
    )
    await sio.emit('reply_message', {'status': 'message sent'})


async def create_socketio():
    await sio.connect('http://localhost:5000', transports=['websocket'])


async def echo_all(message: Message):
    session: AsyncSession = async_session_maker()
    model = {
        'user_id': None,
        'reply_user_id': None,
        'is_reply': False,
        'text': message.text,
        'attachment': None,
        'attachment_type': None,
        'chat_id': message.chat.id
    }
    chat_user: ChatUser | None = await session.scalar(
        select(ChatUser)
        .join(UserSource)
        .where(
            and_(
                ChatUser.platform_id == message.from_user.id,
                UserSource.title == 'Telegram'
            )
    ))
    if not chat_user:
        tg_id: UserSource = await session.scalar(
                    select(UserSource)
                    .where(UserSource.title == 'Telegram')
                )

        new_user: ChatUser = ChatUser()
        new_user.name = message.from_user.full_name
        new_user.user_source_id = tg_id.id
        new_user.platform_id = message.from_user.id
        new_user.platform_login = message.from_user.username
        # new_user: ChatUser = await session.scalar(
        #     insert(ChatUser).returning(ChatUser).values({
        #         'name': message.from_user.full_name,
        #         'user_source_id': tg_id.id,
        #         'platform_id': message.from_user.id,
        #         'platform_login': message.from_user.username,
        #         'banned': False
        #     })
        # )
        session.add(new_user)
        await session.commit()
        model['user_id'] = new_user.id
    else:
        model['user_id'] = chat_user.id

    msg = DBMessage(**model)
    session.add(msg)

    await session.commit()

    await sio.emit('new_message', model, namespace='/')
    print('Message emited')


async def command_help(message: Message):
    commands = {  # command description used in the "help" command
        'start': 'Get used to the bot',
        'help': 'Gives you information about the available commands',
        'sendLongText': 'A test using the \'send_chat_action\' command',
        'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
    }
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    await bot.send_message(cid, help_text)  # send the generated help page


bot.register_message_handler(command_help, commands=['start', 'help', 'commands'])
bot.register_message_handler(command_help, func=lambda message: message.text[0] == '/', content_types=['text'])
bot.register_message_handler(echo_all, func=lambda message: True, content_types=['text'])

if __name__ == '__main__':
    import asyncio

    loop = asyncio.new_event_loop()
    # loop.run_until_complete(create_socketio())
    asyncio.gather(
        loop.run_until_complete(create_socketio()),  # socketio client
        loop.run_until_complete(bot.polling()),  # telebot
    )

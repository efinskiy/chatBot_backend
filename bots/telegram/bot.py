import asyncio
import socketio

from telebot.async_telebot import AsyncTeleBot
from config import TOKEN


bot = AsyncTeleBot(
    TOKEN,
    parse_mode="MARKDOWN",
    colorful_logs=True
)


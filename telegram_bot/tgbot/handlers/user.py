from aiogram import Dispatcher
from aiogram.types import Message


async def user_start(message: Message):
    await message.reply(f"Привет, {message.from_user['first_name']}! Введи название любого города, а я помогу узнать погоду в нем!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
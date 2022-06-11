from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


class Enter_time_post(StatesGroup):
    waiting_for_time = State()


async def admin_start(m: Message):
    await m.reply("Hello, admin!")


async def admin_choose_time(m: Message):
    await m.reply("Hello, admin! Enter time")
    await Enter_time_post.waiting_for_time.set()


async def time_entered(m: Message):
    await m.reply(m.text)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(admin_choose_time, commands=["add_time"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(time_entered,  state=Enter_time_post.waiting_for_time,
                                role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)

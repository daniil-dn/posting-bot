from aiogram import Dispatcher, types
from aiogram.types import Message
from tgbot.services.repository import Repo
from tgbot.services.broadcaster import broadcast
from tgbot.config import load_config


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id, m.from_user.username)
    await m.reply("Hello, user!")



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")


# INSERT INTO user_vacancies(main_part, tags, link, userid, date_time) VALUES
# ('<b>GENERALIST (Indie)</b> 🌎 Удаленно' , '# #UnrealEngine #GameDev #Remote #Indie', 'asdf', 5104338493, CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;
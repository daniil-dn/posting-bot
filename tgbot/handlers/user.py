from aiogram import Dispatcher, types
from aiogram.types import Message
from tgbot.services.repository import Repo
from tgbot.services.broadcaster import broadcast
from tgbot.config import load_config


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id, m.from_user.username)
    await m.reply("Hello, user!")


async def ban_cb(m: Message, repo: Repo):
    print("ban this ")
    config = load_config("tgbot/bot.ini")

    await repo.ban_user(m.from_user.id)
    await broadcast(m.bot, config.tg_bot.admin_ids, f'@{m.from_user.username} is banned')
    user_ban_mes = await m.bot.send_message(config.moder_chat_id, f'User @{m.from_user.username} - {m.from_user.id} is banned.')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(ban_cb, lambda cb: cb.data.find('ban') == 0, state="*")

# INSERT INTO user_vacancies(main_part, tags, link, userid, date_time) VALUES
# ('<b>GENERALIST (Indie)</b> 🌎 Удаленно' , '# #UnrealEngine #GameDev #Remote #Indie', 'asdf', 5104338493, CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;
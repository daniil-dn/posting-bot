from aiogram import Dispatcher, types
from aiogram.types import Message
from tgbot.services.repository import Repo


async def user_start(m: Message, repo: Repo):
    await repo.add_user(m.from_user.id, m.from_user.username)
    print("Hello, user!")


async def moder_message(m: Message, repo: Repo, channel_id: int):
#TODO save vacancies in db and create sctipt for posting
    if m.text.find('#UnrealEngine #GameDev') >= 0:
        await m.bot.send_message(chat_id=channel_id, text=m.text)
        print(m.text)



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(moder_message, content_types=[types.ContentType.TEXT, ], state="*")

# INSERT INTO user_vacancies(main_part, tags, link, userid, date_time) VALUES
# ('<b>GENERALIST (Indie)</b> 🌎 Удаленно' , '# #UnrealEngine #GameDev #Remote #Indie', 'asdf', 5104338493, CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;
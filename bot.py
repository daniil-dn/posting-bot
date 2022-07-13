import asyncio
import json
import logging
import asyncpgx

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config, Config
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.services.broadcaster import broadcast
from tgbot.keyboards.keyboards import KeyboardManager
from tgbot.services.NewVacancyParsing import start_notifing


logger = logging.getLogger(__name__)


async def on_startup(bot, config: Config):
    count = await broadcast(bot, config.tg_bot.admin_ids, 'Бот запущен!')
    return count


async def create_pool(user, password, database, host, echo):
    pool = await asyncpgx.create_pool(database=database, user=user, password=password, host=host)
    return pool


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("tgbot/bot.ini")

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(EnvironmentMiddleware(config.channel_id))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    async def new_vacancy_cb(connection, pid, channel, payload):
        payload = json.loads(payload)
        user_id = payload.get("user_id")
        text = payload.get('main_part')
        tags = payload.get('tags')
        link = payload.get('link')
        vacancy_id = payload.get('id')

        button_link = f"\n\n<a href='{link}'>🌐 Vacancy link</a>" if link else ''

        username = await connection.fetch(
            f'SELECT username from tg_users where user_id = {user_id};')
        username = username[0]["username"]
        # Return list A list of Record instances. If specified, the actual type of list elements would be record_class.

        await broadcast(bot, config.tg_bot.admin_ids, f'NEW Vacancy from @{username}')

        try:
            markup_kb = KeyboardManager.get_default_vacancy_kb(user_id, vacancy_id)
            await bot.send_message(config.moder_chat_id, f"Vacancy from @{username}\n\n{text + button_link + tags}",
                                   parse_mode="html",
                                   disable_web_page_preview=True, reply_markup=markup_kb)
            # vacancy_dict = {'username': username, 'text': text, 'button_link': button_link, 'tags': tags}
        except Exception as err:
            await broadcast(bot, config.tg_bot.admin_ids, str(err), True)
        return

    # Обработчик новых вакансий
    conn_for_listner = await pool.acquire()
    await conn_for_listner.add_listener('insert_vacancy', new_vacancy_cb)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await on_startup(bot, config)
        await dp.start_polling()


    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        tln_conf = load_config("tgbot/bot.ini").telethone
        ioloop = asyncio.get_event_loop()
        tasks = [
            main(),
            start_notifing(tln_conf.api_id, tln_conf.api_hash, tln_conf.to_forward, ['ue', "unreal"],
                           load_config("tgbot/bot.ini"), create_pool)
        ]
        ioloop.run_until_complete(asyncio.wait(tasks))
        ioloop.close()
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

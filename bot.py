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

logger = logging.getLogger(__name__)


async def on_startup(bot, config: Config):
    count = await broadcast(bot, config.tg_bot.admin_ids, 'Бот запущен!')
    return count


async def create_pool(user, password, database, host, echo):
    pool = await asyncpgx.create_pool(database=database, user=user, password=password, host=host)
    return pool


def insert_vacancy_cb(connection, pid, channel, payload):
    payload = json.loads(payload)
    print(payload)
    return


async def check_db(pool):
    conn = await pool.acquire()
    await conn.add_listener('insert_vacancy', insert_vacancy_cb)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config("bot.ini")
    # await asyncio.run(check_db)

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
    await check_db(pool)
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(EnvironmentMiddleware(config.channel_id))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids))
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
        await on_startup(bot, config)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

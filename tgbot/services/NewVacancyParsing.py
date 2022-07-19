import asyncpgx
import asyncio

import telethon.tl.functions.account
from telethon import TelegramClient, sync, events
from tgbot.middlewares.db import Repo


# api_id = 10582137
# api_hash = 'bcc45c276f0c29e35cc5d56422c60e45'
# where_to_send = -1001662034287
async def start_notifing(ioloop, logger, api_id, api_hash, where_to_send, key_phrases_list, config, create_pool,
                         session_name='default_name'):
    client = TelegramClient(session_name, api_id, api_hash)



    client.flood_sleep_threshold = 0
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        echo=False,
    )

    @client.on(events.NewMessage)
    async def all_handler(event):
        try:

            db = await pool.acquire()
            repo = Repo(db)
            chs_list = await repo.list_listened_channel()

            try:
                username = getattr(event.chat, 'username')
                logger.info(f'new message from {username}')
            except AttributeError as err:
                return
            if not username in chs_list:
                return
            for key_phrase in key_phrases_list:
                if event.message.text.lower().find(key_phrase) > -1:
                    print('find a new vacancy on tg')
                    await client.forward_messages(where_to_send, event.message, silent=True)
                    return
        except Exception as err:
            logger.error(err)

    async def update_status():
        while True:
            await client(telethon.tl.functions.account.UpdateStatusRequest(False))
            print('status updated')
            await asyncio.sleep(30)
    try:
        await client.start()
        await update_status()
        await client.run_until_disconnected()
    except Exception as err:
        logger.error(err)

#
# group = 'group_name'
#
# participants = client.get_participants(group)
# users = {}
#
# for partic in client.iter_participants(group):
#     lastname = ""
#     if partic.last_name:
#         lastname = partic.last_name
#     users[partic.id] = partic.first_name + " " + lastname
#
# f = open('messages_from_chat', 'a')

# f.close()

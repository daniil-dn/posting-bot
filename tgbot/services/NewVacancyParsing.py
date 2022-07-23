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
    pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        echo=False,
    )

    async def update_status(client):
        while True:
            # await client(telethon.tl.functions.account.UpdateStatusRequest(False))
            # await client.send_message(entity_update, 'update')
            await asyncio.sleep(30)

    try:

        client = TelegramClient(session_name, api_id, api_hash)
        await client.start()

        @client.on(events.NewMessage)
        async def all_handler(event):
            try:
                try:
                    username = getattr(event.chat, 'username')
                    logger.info(f'new message from {username}')
                except AttributeError as err:
                    return
                db = await pool.acquire()
                repo = Repo(db)
                chs_list = await repo.list_listened_channel()
                if not username in chs_list:
                    await db.close()
                    return
                for key_phrase in key_phrases_list:
                    if event.message.text.lower().find(key_phrase) > -1:
                        print('find a new vacancy on tg')
                        await client.forward_messages(where_to_send, event.message, silent=True)
                        await db.close()
                        return
            except Exception as err:
                logger.error(err)

        await client.run_until_disconnected()
        await client.disconnect()
        # entity_update = await client.get_entity('daniil_dn')
        # await update_status(client)



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

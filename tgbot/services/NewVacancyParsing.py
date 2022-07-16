import asyncpgx
import asyncio
from telethon import TelegramClient, sync, events
from tgbot.middlewares.db import Repo
from telethon import functions, types

# api_id = 10582137
# api_hash = 'bcc45c276f0c29e35cc5d56422c60e45'
# where_to_send = -1001662034287
async def start_notifing(logger, api_id, api_hash, where_to_send, key_phrases_list, config, create_pool,
                         session_name='default_name'):
    client = TelegramClient(session_name, api_id, api_hash)
    await client(functions.account.UpdateStatusRequest(
        offline=False
    ))
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

    try:
        await client.start()
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

import asyncpgx
from telethon import TelegramClient, sync, events


# api_id = 10582137
# api_hash = 'bcc45c276f0c29e35cc5d56422c60e45'
# where_to_send = -1001662034287
async def start_notifing(api_id, api_hash, where_to_send, key_phrases_list, session_name='default_name'):
    client = TelegramClient(session_name, api_id, api_hash)

    @client.on(events.NewMessage)
    async def all_handler(event):
        if not event.is_channel:
            return
        for key_phrase in key_phrases_list:
            if event.message.text.lower().find(key_phrase) > -1:
                print('find a new vacancy on tg')
                await client.forward_messages(where_to_send, event.message)
                return

    await client.start()
    await client.run_until_disconnected()

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

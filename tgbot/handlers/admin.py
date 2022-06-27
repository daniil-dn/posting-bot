from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo
from tgbot.services.broadcaster import broadcast
from tgbot.keyboards.keyboards import KeyboardManager
from tgbot.config import load_config


class Enter_time_post(StatesGroup):
    waiting_for_time = State()


async def admin_start(m: Message):
    await m.reply(f"Hello, {m.from_user.full_name}! \nВызов помощи -> /help",
                  reply_markup=KeyboardManager.get_admin_start_rm())


async def admin_help(m: Message):
    await m.reply("/banlist - вывод забаненых user_idj"
                  "\n/ban ID || ban ID - бан по user_id "
                  "\n/unban ID || unban ID - разабан по user_id"
                  "\n/help - вывод этого окна", parse_mode='html', reply_markup=KeyboardManager.get_admin_start_rm())


async def admin_choose_time(m: Message):
    await m.reply("Hello, admin! Enter time")
    await Enter_time_post.waiting_for_time.set()


async def time_entered(m: Message):
    await m.reply(m.text)


async def show_banlist(m: Message, repo: Repo):
    banlist = await repo.banlist_str()
    await m.reply(banlist)
    await m.delete()


async def unban_user(m: Message = None, repo: Repo = None):
    unban_id_list = m.text.split(' ')
    if unban_id_list[1].isdigit():
        repo_mes = await repo.unban_user(unban_id_list[1])
        if repo_mes:
            await m.reply(f'Юзер ID: {unban_id_list[1]} разбанен')

    else:
        await m.reply(f'{m.text} не выполнена! \nПример: /unban 777777')
        await m.delete()


async def ban_user(m: Message, repo: Repo):
    ban_id_list = m.text.split(' ')
    if ban_id_list[1].isdigit():
        repo_mes = await repo.ban_user(ban_id_list[1])
        if repo_mes:
            await m.reply(f'User ID: {ban_id_list[1]} забанен')

    else:
        await m.reply(f'{m.text} не выполнена! \nПример: /ban 777777')
        await m.delete()


async def ban_cb(cb: CallbackQuery, repo: Repo):
    config = load_config("tgbot/bot.ini")
    cb_data_split = cb.data.split('_')
    user_id = cb_data_split[1]
    vacancy_id = cb.data.split('_')[2]

    # помещает в банлист базы
    await repo.ban_user(user_id)

    # admin broadcast notification
    username = await repo.get_username_from_id(user_id)
    username = username if username else 'without Username'
    await broadcast(cb.bot, config.tg_bot.admin_ids, f'@{username} - {user_id} is banned')

    # После бана меняется кнопка под вакансией
    bnm_kb = KeyboardManager.ban_unban_btn_markup(user_id, vacancy_id=vacancy_id, to_ban=False)
    await cb.message.edit_reply_markup(bnm_kb)

    # уведомление в общий чат о том, что юзер забанен
    if cb.message.text.find('#UnrealEngine') > -1:
        ban_notification_mg = \
            await cb.message.reply(f'User @{cb.from_user.username} - {cb.from_user.id} is banned.',
                                   reply_markup=bnm_kb, parse_mode="html")

async def unban_cb(cb: CallbackQuery, repo: Repo):
    config = load_config("tgbot/bot.ini")
    cb_data_split = cb.data.split('_')
    user_id = cb_data_split[1]
    vacancy_id = cb.data.split('_')[2]
    await repo.unban_user(user_id)
    await broadcast(cb.bot, config.tg_bot.admin_ids, f'@{cb.from_user.username} is unbanned')
    if cb.message.text.find('#UnrealEngine') > -1:
        markup_kb = KeyboardManager.get_default_vacancy_kb(user_id, vacancy_id, to_ban=True)
    else:
        markup_kb = KeyboardManager.ban_unban_btn_markup(user_id, vacancy_id, to_ban=True)
    await cb.message.edit_reply_markup(markup_kb)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(admin_help, commands=["help"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(admin_choose_time, commands=["add_time"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(time_entered, state=Enter_time_post.waiting_for_time,
                                role=UserRole.ADMIN)
    dp.register_callback_query_handler(ban_cb, lambda cb: cb.data.find('ban') == 0, state="*")
    dp.register_callback_query_handler(unban_cb, lambda cb: cb.data.find('unban') == 0, state="*")
    dp.register_message_handler(show_banlist, commands=["banlist"], state="*", role=UserRole.ADMIN)

    # TODO сделать бан и разбан на конечных автоматах
    dp.register_message_handler(unban_user, lambda t: t.text.find('unban') > -1 and t.text.split(' ').__len__() >= 2,
                                state="*",
                                role=UserRole.ADMIN)
    dp.register_message_handler(ban_user, lambda t: t.text.find('ban') > -1 and t.text.split(' ').__len__() >= 2,
                                state="*",
                                role=UserRole.ADMIN)

    dp.register_callback_query_handler(ban_cb, lambda cb: cb.data.find('ban_') == 0, state="*")
    dp.register_callback_query_handler(unban_cb, lambda cb: cb.data.find('unban_') == 0, state="*")
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)

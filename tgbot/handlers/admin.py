from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State

from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

from tgbot.keyboards.keyboards import KeyboardManager


class Enter_time_post(StatesGroup):
    waiting_for_time = State()


async def admin_start(m: Message):
    await m.reply(f"Hello, {m.from_user.full_name}! \nВызов помощи -> /help", reply_markup=KeyboardManager.get_admin_start_rm())

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


async def unban_user(m: Message, repo: Repo):
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


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(admin_help, commands=["help"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(admin_choose_time, commands=["add_time"], state="*", role=UserRole.ADMIN)
    dp.register_message_handler(time_entered, state=Enter_time_post.waiting_for_time,
                                role=UserRole.ADMIN)
    dp.register_message_handler(show_banlist, commands=["banlist"], state="*", role=UserRole.ADMIN)

    # TODO сделать бан и разбан на конечных автоматах
    dp.register_message_handler(unban_user, lambda t: t.text.find('unban') > -1 and t.text.split(' ').__len__() >= 2,
                                state="*",
                                role=UserRole.ADMIN)
    dp.register_message_handler(ban_user, lambda t: t.text.find('ban') > -1 and t.text.split(' ').__len__() >= 2,
                                state="*",
                                role=UserRole.ADMIN)
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)

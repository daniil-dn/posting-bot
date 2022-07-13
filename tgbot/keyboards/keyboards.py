from aiogram import types


class KeyboardManager:

    @staticmethod
    def get_default_vacancy_kb(user_id, vacancy_id, to_ban=True):
        ban_unban_txt = 'Ban' if to_ban else 'Unban'
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(types.InlineKeyboardButton('Publish', callback_data=f'publish_{vacancy_id}'))
        kb.insert(types.InlineKeyboardButton('Reject', callback_data=f'reject_{vacancy_id}'))
        kb.insert(types.InlineKeyboardButton(ban_unban_txt, callback_data=f'ban_{user_id}_{vacancy_id}'))
        return kb

    @staticmethod
    def get_admin_start_rm():
        kb = types.ReplyKeyboardMarkup(row_width=3)
        kb.insert(types.KeyboardButton('/banlist'))
        kb.insert(types.KeyboardButton('/unban ID'))
        kb.insert(types.KeyboardButton('/ban ID'))
        kb.insert(types.KeyboardButton('/add_channel'))
        kb.insert(types.KeyboardButton('/rm_channel'))
        kb.insert(types.KeyboardButton('/show_channels'))
        return kb

    @staticmethod
    def ban_unban_btn_markup(user_id, vacancy_id=False, to_ban=True):
        kb = types.InlineKeyboardMarkup(row_width=3)
        text = 'Ban' if to_ban else 'Unban'
        vacancy_id = f"_vacancy_id" if vacancy_id else ''
        un_or_ban = 'ban' if to_ban else 'unban'
        kb.insert(types.InlineKeyboardButton(text, callback_data=f'{un_or_ban}_{user_id}{vacancy_id}'))
        return kb

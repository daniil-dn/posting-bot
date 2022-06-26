from aiogram import types


class KeyboardManager:

    @staticmethod
    def get_default_vacancy_kb(vacancy_id, user_id):
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(types.InlineKeyboardButton('Publish', callback_data=f'publish_{vacancy_id}'))
        kb.insert(types.InlineKeyboardButton('Reject', callback_data=f'reject_{vacancy_id}'))
        kb.insert(types.InlineKeyboardButton('Ban', callback_data=f'ban_{user_id}'))
        return kb

    @staticmethod
    def get_admin_start_rm():
        kb = types.ReplyKeyboardMarkup(row_width=3)
        kb.insert(types.KeyboardButton('/banlist'))
        kb.insert(types.KeyboardButton('/unban ID'))
        kb.insert(types.KeyboardButton('/ban ID'))
        return kb

    @staticmethod
    def unban_cb_markup(user_id):
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.insert(types.InlineKeyboardButton('Unban', callback_data=f'unban_{user_id}'))
        return kb

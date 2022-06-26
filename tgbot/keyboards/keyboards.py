from aiogram import types


class KeyboardManager:

    @staticmethod
    def get_default_vacancy_kb(vacancy_id):
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(types.InlineKeyboardButton('Publish', callback_data=f'publish_{vacancy_id}'))
        kb.insert(types.InlineKeyboardButton('Reject', callback_data=f'reject_{vacancy_id}'))
        kb.insert(types.InlineKeyboardButton('Ban', callback_data=f'ban_{vacancy_id}'))
        return kb

    @staticmethod
    def get_admin_start_rm():
        kb = types.ReplyKeyboardMarkup(row_width=3)
        kb.insert(types.KeyboardButton('/banlist'))
        return kb
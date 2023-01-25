from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("Droid", callback_data=f'choose_device:android'),
        InlineKeyboardButton("iOS", callback_data=f'choose_device:ios'),
    ],
        [InlineKeyboardButton("PC", callback_data=f'choose_device:pc')]]

    return InlineKeyboardMarkup(buttons)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dtb.settings import PAYMENT_URL


def choose_device() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("📱 Android", callback_data=f'choose_device:android'),
        InlineKeyboardButton("🍎 iOS", callback_data=f'choose_device:ios'),
    ],
        [InlineKeyboardButton("🖥 Компьютер (Windows, Linux, MacOS)", callback_data=f'choose_device:pc')]]

    return InlineKeyboardMarkup(buttons)


def choose_device_pc() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📱 Android", callback_data=f'choose_device:android'),
            InlineKeyboardButton("🍎 iOS", callback_data=f'choose_device:ios'),
        ],
        [InlineKeyboardButton("🖥️ Windows", callback_data=f'choose_device:windows')],
        [InlineKeyboardButton("🍏 MacOS", callback_data=f'choose_device:macos'),
         InlineKeyboardButton("🐧 Linux", callback_data=f'choose_device:linux'), ]
    ]

    return InlineKeyboardMarkup(buttons)


def main_menu(user_id, bot_link) -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("💻 Мои устройства", callback_data=f'my_devices'),
        InlineKeyboardButton("👥 Пригласить друга", url=f'{bot_link}?start={user_id}'),
    ],
        [InlineKeyboardButton("💳 Оплатить", web_app=WebAppInfo(url=PAYMENT_URL))],
        [InlineKeyboardButton("👨‍🔧 Поддержка", callback_data=f'main_menu:support')],
    ]

    return InlineKeyboardMarkup(buttons)

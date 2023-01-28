from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


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


def main_menu() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton("💻 Мои устройства", callback_data=f'main_menu:devices'),
        InlineKeyboardButton("👥 Пригласить друга", callback_data=f'main_menu:invoke_friend'),
    ],
        [InlineKeyboardButton("💳 Оплатить", web_app=WebAppInfo(url='https://vpnbottest.cupsoft.ru/pay/'))],
        [InlineKeyboardButton("👨‍🔧 Поддержка", callback_data=f'main_menu:support')],
    ]

    return InlineKeyboardMarkup(buttons)

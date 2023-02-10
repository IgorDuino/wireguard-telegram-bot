from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dtb.settings import PAYMENT_URL, BOT_LINK

from shop.models import VPNProfile
from users.models import User

from datetime import datetime


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


def main_menu(user: User) -> InlineKeyboardMarkup:
    user_id = user.user_id
    profiles = VPNProfile.objects.filter(user=user)
    payment_id = None
    if len(profiles) == 1:
        payment_id = profiles[0].id_on_server

    buttons = [[
        InlineKeyboardButton("💻 Мои устройства", callback_data=f'profiles'),
        InlineKeyboardButton("👥 Пригласить друга", url=f'{BOT_LINK}?start={user_id}'),
    ],
        [InlineKeyboardButton("💳 Оплатить", callback_data=f'main_menu:choose_profile_to_pay')],
        [InlineKeyboardButton("👨‍🔧 Поддержка", callback_data=f'main_menu:support')],
    ]

    if payment_id:
        buttons[1] = [InlineKeyboardButton("💳 Оплатить", web_app=WebAppInfo(url=f"{PAYMENT_URL}?uid={payment_id}"))]

    return InlineKeyboardMarkup(buttons)


def profiles_menu(user: User) -> InlineKeyboardMarkup:
    profiles = VPNProfile.objects.filter(user=user)
    buttons = []
    for profile in profiles:
        buttons.append(
            [InlineKeyboardButton(f"{profile.name} - оплачен до {datetime.strftime(profile.active_until, '%d.%m.%Y')}",
                                  callback_data=f'profile:{profile.id}')])
    buttons.append([InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu')])
    return InlineKeyboardMarkup(buttons)

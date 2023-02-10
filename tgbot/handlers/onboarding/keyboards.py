from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dtb.settings import PAYMENT_URL, BOT_LINK

from shop.models import VPNProfile
from users.models import User

from datetime import datetime

from typing import List


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
    profile_server_id = None
    if len(profiles) == 1:
        profile_server_id = profiles[0].id_on_server

    buttons = [[
        InlineKeyboardButton("💻 Мои устройства", callback_data=f'profiles'),
        InlineKeyboardButton("👥 Пригласить друга", url=f'{BOT_LINK}?start={user_id}'),
    ],
        [InlineKeyboardButton("💳 Оплатить", callback_data=f'choose_pay_profile')],
        [InlineKeyboardButton("➕ Добавить профиль", callback_data=f'new_profile')],
        [InlineKeyboardButton("👨‍🔧 Поддержка", callback_data=f'support')],
    ]

    if profile_server_id:
        buttons[1] = [InlineKeyboardButton("💳 Оплатить", callback_data=f'choose_pay_period:{profile_server_id}')]
    return InlineKeyboardMarkup(buttons)


def profiles_menu(user: User) -> InlineKeyboardMarkup:
    profiles = VPNProfile.objects.filter(user=user)
    buttons = []
    for profile in profiles:
        buttons.append(
            [InlineKeyboardButton(f"{profile.name} - оплачен до {datetime.strftime(profile.active_until, '%d.%m.%Y')}",
                                  callback_data=f'profile:{profile.id}')])

    buttons.append([InlineKeyboardButton("➕ Добавить профиль", callback_data=f'new_profile')])
    buttons.append([InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu')])
    return InlineKeyboardMarkup(buttons)


def choose_pay_profile_handler(profiles: List[VPNProfile]) -> InlineKeyboardMarkup:
    buttons = []
    for profile in profiles:
        buttons.append([InlineKeyboardButton(f"{profile.name} - Оплачен до {profile.active_until}",
                                             callback_data=f'choose_pay_period:{profile.server_id}')])
    buttons.append([InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu')])
    return InlineKeyboardMarkup(buttons)


def choose_pay_period(profile_server_id) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("1 месяц", callback_data=f'pay:{profile_server_id}:1'),
            InlineKeyboardButton("3 месяца", callback_data=f'pay:{profile_server_id}:3'),
            InlineKeyboardButton("6 месяцев", callback_data=f'pay:{profile_server_id}:6'),
        ],
        [InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu')],
    ]

    return InlineKeyboardMarkup(buttons)


def pay_button(profile: VPNProfile, period: int) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(f"💳 Оплатить профиль {profile.name} на {period} дней", web_app=WebAppInfo(
        url=f"{PAYMENT_URL}?server_id={profile.id_on_server}&period={period}"))]]
    return InlineKeyboardMarkup(buttons)

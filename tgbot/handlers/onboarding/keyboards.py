from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from dtb.settings import PAYMENT_URL, BOT_LINK, TELEGRAPH_INSTRUCTION_LINK

from shop.models import VPNProfile
from users.models import User

from datetime import datetime

from typing import List

import random
import string


def rand_suffix():
    return ''.join([random.choice(string.hexdigits) for _ in range(4)])


def empty_menu():
    return InlineKeyboardMarkup([[]])


def choose_device() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(
            "📱 Android", callback_data=f'choose_device:android:{rand_suffix()}'),
        InlineKeyboardButton(
            "🍎 iOS", callback_data=f'choose_device:ios:{rand_suffix()}'),
    ],
        [InlineKeyboardButton("🖥 Компьютер (Windows, Linux, MacOS)",
                              callback_data=f'choose_device:pc:{rand_suffix()}')]]

    return InlineKeyboardMarkup(buttons)


def choose_device_pc() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📱 Android", callback_data=f'choose_device:android:{rand_suffix()}'),
            InlineKeyboardButton("🍎 iOS", callback_data=f'choose_device:ios:{rand_suffix()}'),
        ],
        [InlineKeyboardButton("🖥️ Windows", callback_data=f'choose_device:windows:{rand_suffix()}')],
        [InlineKeyboardButton("🍏 MacOS", callback_data=f'choose_device:macos:{rand_suffix()}'),
         InlineKeyboardButton("🐧 Linux", callback_data=f'choose_device:linux:{rand_suffix()}'), ]
    ]

    return InlineKeyboardMarkup(buttons)


def main_menu(user: User) -> InlineKeyboardMarkup:
    user_id = user.user_id
    profiles = VPNProfile.objects.filter(user=user)
    profile_server_id = None
    if len(profiles) == 1:
        profile_server_id = profiles[0].id_on_server

    buttons = [[
        InlineKeyboardButton("💻 Мои устройства", callback_data=f'profiles:{rand_suffix()}'),
        InlineKeyboardButton("👥 Пригласить друга", url=f'{BOT_LINK}?start={user_id}'),
    ],
        [InlineKeyboardButton("💳 Оплатить", callback_data=f'choose_pay_profile:{rand_suffix()}')],
        [InlineKeyboardButton("➕ Добавить профиль", callback_data=f'new_profile:{rand_suffix()}')],
        [InlineKeyboardButton("👨‍🔧 Поддержка", callback_data=f'support:{rand_suffix()}')],
    ]

    if profile_server_id:
        buttons[1] = [
            InlineKeyboardButton("💳 Оплатить", callback_data=f'choose_pay_period:{profile_server_id}:{rand_suffix()}')]
    return InlineKeyboardMarkup(buttons)


def profiles_menu(user: User) -> InlineKeyboardMarkup:
    profiles = VPNProfile.objects.filter(user=user)
    buttons = []
    for profile in profiles:
        buttons.append(
            [InlineKeyboardButton(f"{profile.name} - оплачен до {datetime.strftime(profile.active_until, '%d.%m.%Y')}",
                                  callback_data=f'profile:{profile.id}:{rand_suffix()}')])

    buttons.append([InlineKeyboardButton("➕ Добавить профиль", callback_data=f'new_profile:{rand_suffix()}')])
    buttons.append([InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu:{rand_suffix()}')])
    return InlineKeyboardMarkup(buttons)


def profile_menu(profile: VPNProfile) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton("⬇ Скачать файл конфигурации",
                              callback_data=f'download_configuration:{profile.id}:{rand_suffix()}')],
        [InlineKeyboardButton("📝 Инструкция по подключению", url=TELEGRAPH_INSTRUCTION_LINK)],
        [InlineKeyboardButton("🟥 Отказаться от профиля",
                              callback_data=f'cancle_profile_submit:{profile.id}:{rand_suffix()}')],
        [InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu:{rand_suffix()}')]
    ]

    return InlineKeyboardMarkup(buttons)


def choose_pay_profile_handler(profiles: List[VPNProfile]) -> InlineKeyboardMarkup:
    buttons = []
    for profile in profiles:
        buttons.append([InlineKeyboardButton(f"{profile.name} - Оплачен до {profile.active_until}",
                                             callback_data=f'choose_pay_period:{profile.id_on_server}:{rand_suffix()}')])
    buttons.append([InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu:{rand_suffix()}')])
    return InlineKeyboardMarkup(buttons)


def choose_pay_period(profile_server_id) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("1 месяц", callback_data=f'pay:{profile_server_id}:1:{rand_suffix()}'),
            InlineKeyboardButton("3 месяца", callback_data=f'pay:{profile_server_id}:3:{rand_suffix()}'),
            InlineKeyboardButton("6 месяцев", callback_data=f'pay:{profile_server_id}:6:{rand_suffix()}'),
        ],
        [InlineKeyboardButton("🔙 Главное меню", callback_data=f'main_menu:{rand_suffix()}')],
    ]

    return InlineKeyboardMarkup(buttons)


def pay_button(profile: VPNProfile, period: int) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(f"💳 Оплатить профиль {profile.name} на {period} дней", web_app=WebAppInfo(
        url=f"{PAYMENT_URL}?server_id={profile.id_on_server}&period={period}"))]]
    return InlineKeyboardMarkup(buttons)

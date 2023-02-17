from dtb.settings import TRIAL_PERIOD_DAYS


def start_text(first_name, is_first_time):
    if is_first_time:
        text = f"""
Привет, {first_name}!
Я бот, который поможет тебе подключиться к VPN.
Для начала выбери устройство, с которого ты хочешь подключиться к VPN.
        """
    else:
        text = f"""
Привет, {first_name}!
    """

    return text


def after_device_text(device):
    android_instructions = """
1. Скачайте приложение WireGuard для Android
2. Нажмите на кнопку "+", выберите "Импорт конфигурации из файла"
3. Выберите файл .conf
4. Введите любое название туннеля
    """

    ios_instructions = """
1. Скачайте приложение WireGuard для iOS
2. Нажмите на кнопку "+", выберите "Импорт конфигурации из файла"
3. Выберите файл .conf
4. Введите любое название туннеля
    """

    linux_instructions = """
sudo nmcli connection import type wireguard file <path_to_conf_file>
    """

    macos_instructions = """
1. Скачайте приложение WireGuard для macOS
2. Нажмите на кнопку "+", выберите "Импорт конфигурации из файла"
3. Выберите файл .conf
4. Введите любое название туннеля
    """

    windows_instructions = """
1. Скачайте приложение WireGuard для Windows
2. Нажмите на кнопку "+", выберите "Импорт конфигурации из файла"
3. Выберите файл .conf
4. Введите любое название туннеля
    """

    instructions = {
        'android': android_instructions,
        'ios': ios_instructions,
        'macos': macos_instructions,
        'linux': linux_instructions,
        'windows': windows_instructions,
    }

    full_instructions_links = {
        'android': 'https://www.wireguard.com/install/#android',
        'ios': 'https://www.wireguard.com/install/#ios',
        'macos': 'https://www.wireguard.com/install/#macos',
        'linux': 'https://www.wireguard.com/install/#linux',
        'windows': 'https://www.wireguard.com/install/#windows',
    }
    # TODO: write telegra.ph articles

    text = f"""
Пробный период: {TRIAL_PERIOD_DAYS} дня \n
Краткая инструкция по установке на ваше устройство: \n
{instructions[device]} \n
Полная инструкция по установке: {full_instructions_links[device]} \n
    """

    return text


no_available_servers = """Просим прощения, но в данный момент нет доступных серверов. Техническая поддержка уже работает
 над этой проблемой.
"""

server_error = """
Просим прощения, но в данный момент сервер недоступен. Техническая поддержка уже работает над этой проблемой.
"""

no_profiles = """
У вас нет профилей
"""

choose_profile_text = """
Какой профиль вы хотите оплатить?
"""

my_devices_text = """
Ваши профили:
"""

choose_pay_period_text = """
Выберите частоту подписки:
"""

pay_text = """
Оплата через CloudPayments:
"""

new_profile_text = """
Выберите устройство, с которого вы хотите подключиться к VPN:
"""

new_profile_trial_text = """
Нельзя добавить новый профиль во время пробного периода
"""

maximum_profiles_text = """
Вы достигли максимального количества профилей
"""

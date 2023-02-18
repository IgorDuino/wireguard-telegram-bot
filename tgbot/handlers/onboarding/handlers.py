import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
import tgbot.handlers.onboarding.keyboards as keyboards

from shop import text as shop_text
from shop.utils import wireguard_client
from shop.models import VPNServer, VPNProfile

from datetime import datetime, timedelta

from dtb.settings import TRIAL_PERIOD_DAYS, ROOT_ADMIN_ID, MAXIMUM_PROFILES

import random
import string


def callback_minute(context: CallbackContext):
    expired_profiles = VPNProfile.objects.filter(active_until__lt=datetime.now()).all()

    for expired_profile in expired_profiles:
        user: User = expired_profile
        wg = wireguard_client.WireguardApiClient(
            expired_profile.server.wireguard_api_url, expired_profile.server.password)
        wg.disable_client(expired_profile.id_on_server)
        context.bot.send_message(
            user.user_id, shop_text.profile_expire_text.format(profile_name=expired_profile.name))
        expired_profile.delete()



def command_start(update: Update, context: CallbackContext) -> None:
    user, created = User.get_user_and_created(update, context)
    start_code = update.message.text.split(' ')[1] if len(update.message.text.split(' ')) > 1 else None

    text = shop_text.start_text(user.first_name, created)

    if created:
        if start_code:
            user.deep_link = start_code
            user.save()
        keyboard = keyboards.choose_device()
    else:
        keyboard = keyboards.main_menu(user)

    update.message.reply_text(text=text,
                              reply_markup=keyboard)


def command_clear(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    msg = update.message.reply_text(text='Clearing keyboard',
                                    reply_markup=ReplyKeyboardRemove())
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
    context.bot.send_message(chat_id=update.message.chat_id, text='Главное меню',
                             reply_markup=keyboards.main_menu(user))


def choose_device_handler(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)

    device = update.callback_query.data.split(':')[1]

    if device == 'pc':
        update.callback_query.edit_message_reply_markup(reply_markup=keyboards.choose_device_pc())
        return

    # TODO in future: prefer to connect to the same server as user was connected before

    servers = VPNServer.objects.filter(is_active=True).order_by('?').all()

    if len(servers) == 0:
        logging.error(f'No available servers')
        update.callback_query.edit_message_text(text=shop_text.no_available_servers)
        context.bot.send_message(chat_id=ROOT_ADMIN_ID,
                                 text=f'No servers')
        return

    for server in servers:
        try:
            wg = wireguard_client.WireguardApiClient(server.wireguard_api_url, server.password)
            break
        except wireguard_client.AuthError:
            context.bot.send_message(chat_id=ROOT_ADMIN_ID,
                                     text=f'Wireguard server {server} auth error')
            # TODO: mark server as inactive
    else:
        logging.error(f'All servers are unavailable')
        update.callback_query.edit_message_text(text=shop_text.no_available_servers)
        context.bot.send_message(chat_id=ROOT_ADMIN_ID,
                                 text=f'All servers are unavailable')
        return

    new_profile = VPNProfile.objects.create(server=server, user=user)
    new_profile.user = user
    new_profile.created_at = datetime.now()
    new_profile.active_until = new_profile.created_at + timedelta(days=TRIAL_PERIOD_DAYS)

    name = f"{server.city}_{''.join(random.choice(string.ascii_lowercase) for _ in range(10))}{str(new_profile.id)}"
    server_profile = wg.create_profile(name)

    new_profile.name = name
    new_profile.ip = server_profile['address']
    new_profile.id_on_server = server_profile['id']
    new_profile.save()

    config = wg.get_client_configuration(server_profile['id'])
    qr_code = wg.get_client_qr_code(server_profile['id'])

    context.bot.delete_message(
        chat_id=user_id,
        message_id=update.callback_query.message.message_id
    )

    context.bot.send_photo(
        chat_id=user_id,
        photo=qr_code)

    context.bot.send_document(
        chat_id=user_id,
        document=config,
        filename=f'{name}.conf')

    context.bot.send_message(
        chat_id=user_id,
        text=shop_text.after_device_text(device),
        reply_markup=keyboards.main_menu(user)
    )


def profiles_handler(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    profiles = VPNProfile.objects.filter(user=user)
    if not profiles:
        update.callback_query.edit_message_text(shop_text.no_profiles, reply_markup=keyboards.main_menu(user))
        return

    update.callback_query.edit_message_text(shop_text.my_devices_text, reply_markup=keyboards.profiles_menu(user))


def profile_handler(update: Update, context: CallbackContext) -> None:
    profile_id = update.callback_query.data.split(':')[1]
    profile = VPNProfile.objects.filter(id=profile_id).first()
    update.callback_query.edit_message_text(f"Профиль {profile.name}",
                                            reply_markup=keyboards.profile_menu(profile))


def download_configuration_handler(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    profile_id = update.callback_query.data.split(':')[1]
    profile = VPNProfile.objects.filter(id=profile_id).first()

    wg = wireguard_client.WireguardApiClient(profile.server.wireguard_api_url, profile.server.password)
    config = wg.get_client_configuration(profile.id_on_server)

    update.callback_query.delete_message()
    context.bot.send_document(
        chat_id=update.callback_query.message.chat_id,
        caption="Файл конфигурации",
        document=config,
        filename=f'{profile.name}.conf',
    )
    context.bot.send_message(update.callback_query.message.chat_id,
                             f"Профиль {profile.name}",
                             reply_markup=keyboards.profile_menu(profile))


def main_menu_send(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)
    update.callback_query.edit_message_reply_markup(reply_markup=keyboards.main_menu(user))


def choose_pay_period_handler(update: Update, context: CallbackContext) -> None:
    profile_server_id = update.callback_query.data.split(':')[1]
    profile = VPNProfile.objects.filter(id_on_server=profile_server_id).first()

    if profile:
        update.callback_query.edit_message_text(text=shop_text.choose_pay_period_text,
                                                reply_markup=keyboards.choose_pay_period(profile_server_id))


def choose_pay_profile_handler(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)
    profiles = VPNProfile.objects.filter(user=user).all()
    if not profiles:
        update.callback_query.edit_message_text(shop_text.no_profiles, reply_markup=keyboards.main_menu(user))
        return
    update.callback_query.edit_message_text(text=shop_text.choose_profile_text,
                                            reply_markup=keyboards.choose_pay_profile_handler(profiles))


def pay_handler(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    profile_server_id = update.callback_query.data.split(':')[1]
    logging.warning(f'profile_server_id: {profile_server_id}')
    profile = VPNProfile.objects.filter(id_on_server=profile_server_id).first()
    logging.warning(f'profile: {profile}')
    period = int(update.callback_query.data.split(':')[2]) * 30
    update.callback_query.edit_message_text(text=shop_text.pay_text,
                                            reply_markup=keyboards.pay_button(profile, period))


def new_profile_handler(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)
    if user.is_trial:
        context.bot.send_message(user.user_id, shop_text.new_profile_trial_text)
        return
    if VPNProfile.objects.filter(user=user).count() >= MAXIMUM_PROFILES:
        context.bot.send_message(user.user_id, shop_text.maximum_profiles_text)
        return

    update.callback_query.edit_message_text(shop_text.new_profile_text, reply_markup=keyboards.choose_device())

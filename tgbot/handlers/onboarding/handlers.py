import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import choose_device, choose_device_pc, main_menu

from shop import text as shop_text
from shop.utils import wireguard_client
from shop.models import VPNServer, VPNProfile

from datetime import datetime, timedelta

from dtb.settings import TRIAL_PERIOD_DAYS

import random
import string


def command_start(update: Update, context: CallbackContext) -> None:
    user, created = User.get_user_and_created(update, context)
    start_code = update.message.text.split(' ')[1] if len(update.message.text.split(' ')) > 1 else None

    text = shop_text.start_text(user.first_name, created)

    bot_link = f"https://t.me/{context.bot.username}"
    if created:
        if start_code:
            user.deep_link = start_code
            user.save()
        keyboard = choose_device()
    else:
        keyboard = main_menu(bot_link=bot_link, user=user)

    update.message.reply_text(text=text,
                              reply_markup=keyboard)


def command_clear(update: Update, context: CallbackContext) -> None:
    user = User.get_user(update, context)

    msg = update.message.reply_text(text='Clearing keyboard',
                                    reply_markup=ReplyKeyboardRemove())
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=msg.message_id)
    context.bot.send_message(chat_id=update.message.chat_id, text='Главное меню',
                             reply_markup=main_menu(bot_link=f"https://t.me/{context.bot.username}",
                                                    user=user))


def choose_device_handler(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)

    device = update.callback_query.data.split(':')[1]

    if device == 'pc':
        update.callback_query.edit_message_reply_markup(reply_markup=choose_device_pc())
        return

    # TODO in future: prefer to connect to the same server as user was connected before

    server = VPNServer.objects.filter(is_active=True).order_by('?').first()

    if server is None:
        logging.error(f'No available servers {server}')
        update.callback_query.edit_message_text(text=shop_text.no_available_servers)
        # TODO: send message to support
        return

    try:
        wg = wireguard_client.WireguardApiClient(server.wireguard_api_url, server.password)
    except wireguard_client.AuthError:
        # TODO: send message to support
        # TODO in future: add server to blacklist
        # TODO in future: try to connect to another server
        update.callback_query.edit_message_text(text=shop_text.server_error)
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

    bot_link = f"https://t.me/{context.bot.username}"
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
        reply_markup=main_menu(bot_link=bot_link, user=user)
    )

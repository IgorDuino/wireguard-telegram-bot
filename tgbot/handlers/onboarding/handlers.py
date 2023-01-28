from telegram import Update
from telegram.ext import CallbackContext

from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import choose_device, choose_device_pc, main_menu

from shop import text as shop_text
from shop.utils import wireguard_client
from shop.models import VPNServer, VPNProfile

import random
import string


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    text = shop_text.start_text(u.first_name, created)

    if created:
        keyboard = choose_device()
    else:
        keyboard = main_menu()

    update.message.reply_text(text=text,
                              reply_markup=keyboard)


def choose_device_handler(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    user = User.get_user(update, context)

    device = update.callback_query.data.split(':')[1]

    if device == 'pc':
        update.callback_query.edit_message_reply_markup(reply_markup=choose_device_pc())
        return

    # TODO: select server to connect user
    # TODO in future: prefer to connect to the same server as user was connected before
    # get random server for now
    server = VPNServer.objects.filter(is_active=True).order_by('?').first()
    if server is None:
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

    name = f"{server.city}_{''.join(random.choice(string.ascii_lowercase) for _ in range(10))}{str(new_profile.id)}"
    server_profile = wg.create_profile(name)
    print(server_profile)

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
        reply_markup=main_menu()
    )

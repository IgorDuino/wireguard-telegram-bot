from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.main import bot


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # Usual commands
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
    dp.add_handler(CommandHandler("clear", onboarding_handlers.command_clear))

    # Admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))

    # Keyboard handlers
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.choose_device_handler,
                                        pattern=lambda x: x.startswith('choose_device:')))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.new_profile_handler,
                                        pattern='new_profile'))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.profiles_handler,
                                        pattern='profiles'))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.main_menu_send, pattern='main_menu'))

    dp.add_handler(CallbackQueryHandler(onboarding_handlers.choose_pay_period_handler,
                                        pattern=lambda x: x.startswith('choose_pay_period:')))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.choose_pay_profile_handler,
                                        pattern='choose_pay_profile'))
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.pay_handler,
                                        pattern=lambda x: x.startswith('pay:')))

    # broadcast message
    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'),
                       broadcast_handlers.broadcast_command_with_message)
    )
    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))

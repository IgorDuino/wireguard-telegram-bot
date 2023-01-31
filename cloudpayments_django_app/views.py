from django.shortcuts import render
from dtb.settings import CLOUDPAYMENTS_PUBLIC_ID, SUBSCRIPTION_PRICE
from garpix_cloudpayments.models.choices import PAYMENT_STATUS_COMPLETED, PAYMENT_STATUS_CANCELLED, \
    PAYMENT_STATUS_DECLINED
from tgbot.main import bot
from dtb.settings import ROOT_ADMIN_ID


def index(request):
    return render(request, 'pay.html', {"public_id": CLOUDPAYMENTS_PUBLIC_ID, "subscription_price": SUBSCRIPTION_PRICE})


def payment_status_changed_callback(payment):
    bot.send_message(chat_id=ROOT_ADMIN_ID, text=f'Статус платежа: {payment.status}')
    if payment.status == PAYMENT_STATUS_COMPLETED:
        print('Меняем статус заказа на успешный')
    elif payment.status in (PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_DECLINED):
        print('Заказ провален')
    else:
        print('Можем тоже использовать')

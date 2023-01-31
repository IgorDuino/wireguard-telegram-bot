from django.shortcuts import render
from dtb.settings import CLOUDPAYMENTS_PUBLIC_KEY
from garpix_cloudpayments.models.choices import PAYMENT_STATUS_COMPLETED, PAYMENT_STATUS_CANCELLED, \
    PAYMENT_STATUS_DECLINED


def index(request):
    return render(request, 'pay.html', {"public_key": CLOUDPAYMENTS_PUBLIC_KEY})


def payment_status_changed_callback(payment):
    if payment.status == PAYMENT_STATUS_COMPLETED:
        print('Меняем статус заказа на успешный')
    elif payment.status in (PAYMENT_STATUS_CANCELLED, PAYMENT_STATUS_DECLINED):
        print('Заказ провален')
    else:
        print('Можем тоже использовать')

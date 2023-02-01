from django.shortcuts import render, HttpResponse
from dtb.settings import CLOUDPAYMENTS_PUBLIC_ID, CLOUDPAYMENTS_PRIVATE_KEY, SUBSCRIPTION_PRICE
from tgbot.main import bot
from dtb.settings import ROOT_ADMIN_ID
import hashlib
import hmac
import base64
import json


def index(request):
    uid = request.GET.get('uid')
    if not uid:
        return HttpResponse('uid is required')
    return render(request, 'pay.html', {"public_id": CLOUDPAYMENTS_PUBLIC_ID,
                                        "subscription_price": SUBSCRIPTION_PRICE,
                                        "uid": uid})


def check(request):
    if request.method != 'POST':
        return HttpResponse('Only POST allowed', status=405)

    message = request.read()
    print(message)
    secret = bytes(str(CLOUDPAYMENTS_PRIVATE_KEY), 'utf-8')

    signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())

    print(signature)
    print(request.headers.get('Content-HMAC'))
    if signature == request.headers.get('X-Content-Hmac'):
        print('OK')
        bot.send_message(ROOT_ADMIN_ID, 'OK')
    else:
        print('FAIL')
        bot.send_message(ROOT_ADMIN_ID, 'FAIL')

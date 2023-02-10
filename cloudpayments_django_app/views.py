from django.http import HttpRequest, QueryDict, JsonResponse
from django.shortcuts import render, HttpResponse
from dtb.settings import CLOUDPAYMENTS_PUBLIC_ID, CLOUDPAYMENTS_SECRET_KEY, SUBSCRIPTION_PRICE
from utils.ip import get_client_ip
from cloudpayments_django_app.models import Replenishment
from shop.models import VPNProfile
import ipaddress
import hashlib
import hmac
import base64
from datetime import datetime, timedelta
import logging

CLOUDPAYMENTS_IPS = ["91.142.84.0/27", "87.251.91.160/27", "185.98.81.0/28"]


def check_signature(request: HttpRequest):
    signature = base64.b64encode(
        hmac.new(CLOUDPAYMENTS_SECRET_KEY.encode('utf-8'), request.read(), digestmod=hashlib.sha256).digest())

    check_hmac = signature.decode('utf-8') == request.headers.get('Content-HMAC')

    check_ip = False
    for ip in CLOUDPAYMENTS_IPS:
        if ipaddress.ip_address(get_client_ip(request)) in ipaddress.ip_network(ip, strict=False):
            check_ip = True
            break

    return check_hmac and check_ip


def index(request: HttpRequest):
    uid = request.GET.get('uid')
    if not uid:
        return HttpResponse('uid is required')
    return render(request, 'pay.html', {"public_id": CLOUDPAYMENTS_PUBLIC_ID,
                                        "subscription_price": SUBSCRIPTION_PRICE,
                                        "uid": uid})


# TODO: use django form instead of QueryDict
def check(request: HttpRequest):
    data = QueryDict(request.body)
    amount = float(data["Amount"])
    transaction_id = data["TransactionId"]

    if not check_signature(request):
        return HttpResponse('Forbidden', status=403)

    try:
        if Replenishment.objects.filter(transaction_id=transaction_id).exists():
            logging.warning(f'Replenishment already exists: {transaction_id}')
            return JsonResponse({"code": 10})

        if not VPNProfile.objects.filter(id_on_server=data['AccountId']).exists():
            logging.warning(f'VPNProfile not found: {data["AccountId"]}')
            return JsonResponse({"code": 11})

        if (amount not in [SUBSCRIPTION_PRICE, SUBSCRIPTION_PRICE * 3, SUBSCRIPTION_PRICE * 6]) \
                or data["Currency"] != "RUB":
            logging.warning(f'Wrong amount or currency: {amount} {data["Currency"]}')
            return JsonResponse({"code": 12})

        Replenishment.objects.create(
            amount=amount,
            transaction_id=transaction_id,
            date_time=datetime.strptime(data["DateTime"], "%Y-%m-%d %H:%M:%S"),
            card_first_six=data["CardFirstSix"],
            card_last_four=data["CardLastFour"],
            card_type=data["CardType"],
            card_exp_date=data["CardExpDate"],
            vpn_profile=VPNProfile.objects.get(id_on_server=data['AccountId']),
            subscription_id=data.get("SubscriptionId"),
            ip_address=data.get("IpAddress"),
            payment_method=data.get("PaymentMethod"),
            is_test=data["TestMode"]
        )
        logging.warning(f'New replenishment: {transaction_id}')
        return JsonResponse({"code": 0})

    except Exception as e:
        logging.error(f'Error in check: {e} {data}')
        return JsonResponse({"code": 13})


def pay(request: HttpRequest):
    data = QueryDict(request.body)
    amount = float(data["Amount"])
    transaction_id = data["TransactionId"]

    if not check_signature(request):
        return HttpResponse('Forbidden', status=403)

    replenishment = Replenishment.objects.get(transaction_id=transaction_id)
    if data["Status"] == "Completed":
        replenishment.paid = True
        replenishment.save()

        vpn_profile = replenishment.vpn_profile

        if amount == SUBSCRIPTION_PRICE:
            vpn_profile.active_until += timedelta(days=30)
        elif amount == SUBSCRIPTION_PRICE * 3:
            vpn_profile.active_until += timedelta(days=30 * 3)
        elif amount == SUBSCRIPTION_PRICE * 6:
            vpn_profile.active_until += timedelta(days=30 * 6)

        vpn_profile.save()

        user = vpn_profile.user
        bot.send_message(user.telegram_id,
                         f'Оплата прошла успешно, профиль {vpn_profile.name} продлён до '
                         f'{vpn_profile.active_until.strftime("%d.%m.%Y")}',
                         reply_markup=main_menu(user))

        return JsonResponse({"code": 0})

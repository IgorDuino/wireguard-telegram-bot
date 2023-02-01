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

CLOUDPAYMENTS_IPS = ["91.142.84.0/27", "87.251.91.160/27", "185.98.81.0/28"]


def check_signature(request):
    signature = base64.b64encode(
        hmac.new(bytes(str(CLOUDPAYMENTS_SECRET_KEY), 'utf-8'), request.read(), digestmod=hashlib.sha256).digest())

    check_hmac = signature.decode('utf-8') == request.headers.get('Content-HMAC')

    check_ip = False
    for ip in CLOUDPAYMENTS_IPS:
        if ipaddress.ip_address(get_client_ip(request)) in ipaddress.ip_network(ip):
            check_ip = True
            break

    return check_hmac and check_ip


def index(request):
    uid = request.GET.get('uid')
    if not uid:
        return HttpResponse('uid is required')
    return render(request, 'pay.html', {"public_id": CLOUDPAYMENTS_PUBLIC_ID,
                                        "subscription_price": SUBSCRIPTION_PRICE,
                                        "uid": uid})


def check(request):
    if not check_signature(request):
        return HttpResponse('Forbidden', status=403)

    data = request.POST.dict()
    try:
        if Replenishment.objects.filter(transaction_id=data['TransactionId']).exists():
            return HttpResponse({"code": 10}, content_type='application/json')

        if not VPNProfile.objects.filter(id_on_server=data['AccountId']).exists():
            return HttpResponse({"code": 11}, content_type='application/json')

        if (int(data["Amount"]) not in [SUBSCRIPTION_PRICE, SUBSCRIPTION_PRICE * 2, SUBSCRIPTION_PRICE * 6]) \
                or data["Currency"] != "RUB":
            return HttpResponse({"code": 12}, content_type='application/json')

        Replenishment.objects.create(
            amount=data["Amount"],
            transaction_id=data["TransactionId"],
            date_time=datetime.strptime(data["DateTime"], "%Y-%m-%dT %H:%M:%S"),
            card_first_six=data["CardFirstSix"],
            card_last_four=data["CardLastFour"],
            card_type=data["CardType"],
            card_exp_date=data["CardExpDate"],
            vpn_profile=VPNProfile.objects.get(id_on_server=data['AccountId']),
            subscription_id=data.get("SubscriptionId"),
            ip_address=data.get("IpAddress"),
            payment_method=data.get("PaymentMethod"),
            is_test=data["IsTest"]
        )

    except:
        return HttpResponse({"code": 13}, content_type='application/json')


def pay(request):
    if not check_signature(request):
        return HttpResponse('Forbidden', status=403)

    data = request.POST.dict()
    replenishment = Replenishment.objects.get(transaction_id=data['TransactionId'])
    if data["Status"] == "Completed":
        replenishment.paid = True
        replenishment.save()

        vpn_profile = replenishment.vpn_profile

        if int(data["Amount"]) == SUBSCRIPTION_PRICE:
            vpn_profile.active_until += timedelta(days=30)
        elif int(data["Amount"]) == SUBSCRIPTION_PRICE * 2:
            vpn_profile.active_until += timedelta(days=30 * 2)
        elif int(data["Amount"]) == SUBSCRIPTION_PRICE * 6:
            vpn_profile.active_until += timedelta(days=30 * 6)

        return HttpResponse({"code": 0}, content_type='application/json')

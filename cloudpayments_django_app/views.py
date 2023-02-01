from django.shortcuts import render, HttpResponse
from dtb.settings import CLOUDPAYMENTS_PUBLIC_ID, CLOUDPAYMENTS_SECRET_KEY, SUBSCRIPTION_PRICE
from utils.ip import get_client_ip
import ipaddress
import hashlib
import hmac
import base64

CLOUDPAYMENTS_IPS = ["91.142.84.0/27", "87.251.91.160/27", "185.98.81.0/28"]


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

    signature = base64.b64encode(
        hmac.new(bytes(str(CLOUDPAYMENTS_SECRET_KEY), 'utf-8'), request.read(), digestmod=hashlib.sha256).digest())

    check_hmac = signature.decode('utf-8') == request.headers.get('Content-HMAC')

    check_ip = False
    for ip in CLOUDPAYMENTS_IPS:
        if ipaddress.ip_address(get_client_ip(request)) in ipaddress.ip_network(ip):
            check_ip = True
            break

    if not (check_hmac and check_ip):
        print(check_hmac, check_ip)
        return HttpResponse('Forbidden', status=403)

    return HttpResponse('OK')

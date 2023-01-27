from django.shortcuts import render
import os

public_key = os.environ.get('CLOUDPAYMENTS_PUBLIC_KEY', default=False)


def index(request):
    return render(request, 'pay.html', {"public_key": public_key})

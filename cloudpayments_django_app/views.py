from django.shortcuts import render
import os

api_public = os.environ.get('CLOUDPAYMENTS_PUBLIC_KEY', default=False)


def index(request):
    return render(request, 'pay.html', {"api_public": api_public})

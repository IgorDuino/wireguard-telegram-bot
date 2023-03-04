from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("check", csrf_exempt(views.check)),
    path("pay", csrf_exempt(views.pay)),
]

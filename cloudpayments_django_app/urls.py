from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cloudpayments/', include('garpix_cloudpayments.urls')),
]

import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from cloudpayments_django_app.views import index as pay_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('settings/', include('dbsettings.urls')),
    path('cloudpayments/', include('cloudpayments_django_app.urls')),
    path('pay', pay_view),
]

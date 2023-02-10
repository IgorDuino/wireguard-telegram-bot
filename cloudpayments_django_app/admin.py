from django.contrib import admin
from cloudpayments_django_app.models import Replenishment


@admin.register(Replenishment)
class ReplenishmentAdmin(admin.ModelAdmin):
    pass

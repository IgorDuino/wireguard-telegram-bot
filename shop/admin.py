from django.contrib import admin
from shop.models import VPNProfile, VPNServer


@admin.register(VPNProfile)
class VPNProfileAdmin(admin.ModelAdmin):
    readonly_fields = [
        "name",
        "is_active",
        "id_on_server",
        "ip",
        "server",
    ]


@admin.register(VPNServer)
class VPNServerAdmin(admin.ModelAdmin):
    pass

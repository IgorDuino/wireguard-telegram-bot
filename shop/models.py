from django.db import models


class VPNServer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=255, null=True)
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField(default=True)
    wireguard_api_url = models.URLField(null=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class VPNProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    server = models.ForeignKey(VPNServer, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    ip = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True)
    active_until = models.DateTimeField(null=True)
    id_on_server = models.CharField(max_length=255, null=True)

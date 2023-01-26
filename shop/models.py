from django.db import models


class VPNServer(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    password = models.CharField(max_length=255)
    profiles =

    def __str__(self):
        return self.name


class VPNProfile(models.Model):
    name = models.CharField(max_length=255)
    server = models.ForeignKey(VPNServer, on_delete=models.CASCADE, related_name='profiles')



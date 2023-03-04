from django.db import models


class Replenishment(models.Model):
    amount = models.FloatField()
    transaction_id = models.IntegerField()
    date_time = models.DateTimeField()
    card_first_six = models.CharField(max_length=6)
    card_last_four = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20)
    card_exp_date = models.CharField(max_length=5)
    vpn_profile = models.ForeignKey(
        "shop.VPNProfile", on_delete=models.SET_NULL, null=True
    )
    subscription_id = models.CharField(max_length=512, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    payment_method = models.CharField(max_length=512, null=True)
    is_test = models.BooleanField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.amount} {self.vpn_profile} {"TEST" if self.is_test else ""}'

    class Meta:
        verbose_name = "Replenishment"
        verbose_name_plural = "Replenishments"

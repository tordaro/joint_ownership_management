from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _


class SpotPrice(models.Model):
    """Model for electric spot price in given price area."""

    nok_pr_kwh = models.DecimalField(_("Price per kWh [NOK/kWh]"), max_digits=10, decimal_places=7)
    start_time = models.DateTimeField(_("Start time"))
    price_area = models.IntegerField(_("Price area"))

    eur_pr_kwh = models.DecimalField(_("Price per kWh [EUR/kWh]"), max_digits=10, decimal_places=7, null=True, blank=True)
    exchange_rate = models.DecimalField(_("Exchange rate"), max_digits=10, decimal_places=7, null=True, blank=True)
    end_time = models.DateTimeField(_("End time"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def get_price(self) -> Decimal:
        return self.nok_pr_kwh

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "spot_price"
        ordering = ["-start_time"]
        unique_together = ["start_time", "price_area"]
        indexes = [models.Index(fields=["start_time"]), models.Index(fields=["price_area"]), models.Index(fields=["start_time", "price_area"])]
        verbose_name = _("Spot Price")
        verbose_name_plural = _("Spot Prices")

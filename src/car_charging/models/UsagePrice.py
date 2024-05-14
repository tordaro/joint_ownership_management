from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UsagePrice(models.Model):
    nok_pr_kwh = models.DecimalField(_("Price per kWh [NOK/kWh]"), max_digits=10, decimal_places=7)
    start_date = models.DateField(_("Start date"), unique=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def get_price(self, timestamp: datetime) -> Decimal:
        if timestamp.date() < self.start_date:
            raise ValidationError("Timestamp must be greater than start date.")
        return self.nok_pr_kwh

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = "usage_price"
        verbose_name = _("Usage price")
        verbose_name_plural = _("Usage prices")
        ordering = ["-start_date"]

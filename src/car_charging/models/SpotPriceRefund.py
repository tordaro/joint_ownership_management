from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class SpotPriceRefund(models.Model):
    deduction_threshold = models.DecimalField(_("Deduction thershold [NOK/kWh]"), max_digits=10, decimal_places=7)
    reduction_factor = models.DecimalField(_("Reduction factor"), max_digits=10, decimal_places=7)
    start_date = models.DateField(_("Start date"), unique=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def calculate_refund_price(self, timestamp: datetime, spot_price_nok: Decimal) -> Decimal:
        if timestamp.date() < self.start_date:
            raise ValidationError("Timestamp must be greater than start date.")
        if spot_price_nok <= self.deduction_threshold:
            return Decimal(0)
        return (spot_price_nok - self.deduction_threshold) * self.reduction_factor

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = "spot_price_refund"
        verbose_name = _("Spot price refund")
        verbose_name_plural = _("Spot price refunds")
        ordering = ["-start_date"]

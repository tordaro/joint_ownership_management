from datetime import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class GridPrice(models.Model):
    day_fee = models.DecimalField(_("Day fee per kWh [NOK/kWh]"), max_digits=10, decimal_places=7)
    night_fee = models.DecimalField(_("Night fee per kWh [NOK/kWh]"), max_digits=10, decimal_places=7)
    day_hour_from = models.IntegerField(_("Start hour for day fee"), validators=[MinValueValidator(0), MaxValueValidator(23)])
    night_hour_from = models.IntegerField(_("Start hour for night fee"), validators=[MinValueValidator(0), MaxValueValidator(23)])
    start_date = models.DateField(_("Start date"), unique=True)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def get_price(self, timestamp: datetime) -> Decimal:
        if timestamp.date() < self.start_date:
            raise ValidationError("Timestamp must be greater than start date.")

        if self.day_hour_from <= timestamp.hour < self.night_hour_from:
            return self.day_fee
        else:
            return self.night_fee

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        db_table = "grid_price"
        verbose_name = _("Grid price")
        verbose_name_plural = _("Grid prices")
        ordering = ["-start_date"]

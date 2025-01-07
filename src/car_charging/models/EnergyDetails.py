from django.db import models
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from car_charging.managers.energy_details_manager import EnergyDetailsManager


class EnergyDetails(models.Model):
    objects = EnergyDetailsManager()
    charging_session = models.ForeignKey("ChargingSession", on_delete=models.CASCADE)
    energy = models.DecimalField(max_digits=10, decimal_places=6, verbose_name=_("Energy [kWh]"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def get_hourly_timestamp(self) -> datetime:
        """Get the timestamp with hourly precision."""
        return self.timestamp.replace(minute=0, second=0, microsecond=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "energy_details"
        unique_together = ["charging_session", "timestamp"]
        ordering = ["-timestamp"]
        verbose_name = _("Energy Detail")
        verbose_name_plural = _("Energy Details")

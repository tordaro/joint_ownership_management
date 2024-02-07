from django.db import models
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from car_charging.models.SpotPrices import SpotPrices


class EnergyDetails(models.Model):
    charging_session = models.ForeignKey("ChargingSession", on_delete=models.CASCADE)
    spot_price = models.ForeignKey("SpotPrices", on_delete=models.SET_NULL, null=True)
    energy = models.DecimalField(max_digits=8, decimal_places=6, verbose_name=_("Energy [kWh]"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def set_spot_price(self) -> None:
        """Set the spot price for the given energy detail."""
        self.spot_price = SpotPrices.objects.get(start_time=self.get_hour())
        self.save()

    def get_price(self) -> float | None:
        """Get the price for the given price area, if present."""
        if self.spot_price is not None:
            return self.spot_price.get_price(self.charging_session.price_area)  # The price in for the given price area may be null
        else:
            return None

    def calculate_cost(self) -> float:
        """Calculate the cost of the energy, if spot price is not null."""
        if self.spot_price is not None:
            return self.get_price() * self.energy
        else:
            raise ValueError(f"Spot price for energy detail {self.id} is not set.")

    def get_hour(self) -> datetime:
        """Get the hour for the given timestamp, if spot price is not null."""
        return self.timestamp.replace(minute=0, second=0, microsecond=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "energy_details"
        unique_together = ["charging_session", "timestamp"]
        ordering = ["timestamp"]
        verbose_name = _("Energy Detail")
        verbose_name_plural = _("Energy Details")

from django.db import models
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from car_charging.models.SpotPrices import SpotPrices
from car_charging.managers.energy_details_manager import EnergyDetailsManager


class EnergyDetails(models.Model):
    objects = EnergyDetailsManager()
    charging_session = models.ForeignKey("ChargingSession", on_delete=models.CASCADE)
    spot_price = models.ForeignKey("SpotPrices", on_delete=models.SET_NULL, null=True)
    energy = models.DecimalField(max_digits=8, decimal_places=6, verbose_name=_("Energy [kWh]"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))
    cost = models.DecimalField(max_digits=8, decimal_places=6, editable=False, null=True, verbose_name=_("Cost [kr]"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def set_spot_price(self) -> None:
        """Set the spot price for the given energy detail."""
        self.spot_price = SpotPrices.objects.get(start_time=self.get_hour())

    def get_price(self) -> float:
        """Get the price for the given price area. Raise ValueError if spot price is not available."""
        if self.spot_price is None:
            raise ValueError(f"Spot price for energy detail {self.id} is not set.")
        price = self.spot_price.get_price(self.charging_session.price_area)
        if price is None:
            raise ValueError(f"Price for the given price area in energy detail {self.id} is not available.")
        return price

    def calculate_cost(self) -> float:
        """Calculate the cost of the energy, if spot price is not null."""
        return float(self.get_price()) * float(self.energy)

    def get_hour(self) -> datetime:
        """Get the hour for the given timestamp, if spot price is not null."""
        return self.timestamp.replace(minute=0, second=0, microsecond=0)

    def set_cost(self) -> None:
        """Set calculate and set the cost field."""
        self.cost = self.calculate_cost()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "energy_details"
        unique_together = ["charging_session", "timestamp"]
        ordering = ["timestamp"]
        verbose_name = _("Energy Detail")
        verbose_name_plural = _("Energy Details")

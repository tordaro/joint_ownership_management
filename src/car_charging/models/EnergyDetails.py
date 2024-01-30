from django.db import models
from django.utils.translation import gettext_lazy as _


class EnergyDetails(models.Model):
    charging_session = models.ForeignKey("ChargingSession", on_delete=models.CASCADE)
    spot_price = models.ForeignKey("SpotPrices", on_delete=models.SET_NULL, null=True)
    energy = models.DecimalField(max_digits=8, decimal_places=6, verbose_name=_("Energy"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def get_price(self) -> float | None:
        """Get the price for the given price area."""
        if self.spot_price is not None:
            return self.spot_price.get_price(self.charging_session.price_area)
        else:
            return None

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "energy_details"
        unique_together = ["charging_session", "timestamp"]
        ordering = ["timestamp"]
        verbose_name = _("Energy Detail")
        verbose_name_plural = _("Energy Details")

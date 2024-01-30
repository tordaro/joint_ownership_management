from django.db import models
from django.utils.translation import gettext_lazy as _


class SpotPrices(models.Model):
    """Model definition for electric spot prices in all price areas."""

    no1 = models.DecimalField(_("Price area 1"), max_digits=10, decimal_places=7, blank=True, null=True)
    no2 = models.DecimalField(_("Price area 2"), max_digits=10, decimal_places=7, blank=True, null=True)
    no3 = models.DecimalField(_("Price area 3"), max_digits=10, decimal_places=7, blank=True, null=True)
    no4 = models.DecimalField(_("Price area 4"), max_digits=10, decimal_places=7, blank=True, null=True)
    no5 = models.DecimalField(_("Price area 5"), max_digits=10, decimal_places=7, blank=True, null=True)
    start_time = models.DateTimeField(_("Start time"), unique=True)
    end_time = models.DateTimeField(_("End time"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def get_price(self, price_area: int) -> float:
        """Get the price for the given price area."""
        price_area_name = f"no{price_area}"
        return getattr(self, price_area_name)

    def set_price(self, price_area: int, price: float) -> None:
        """Set the price for the given price area."""
        price_area_name = f"no{price_area}"
        setattr(self, price_area_name, price)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "spot_prices"
        ordering = ["start_time"]
        verbose_name = _("Spot Prices")
        verbose_name_plural = _("Spot Prices")

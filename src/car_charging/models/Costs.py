from django.db import models
from django.utils.translation import gettext_lazy as _


class Costs(models.Model):
    energy_detail = models.OneToOneField("EnergyDetails", on_delete=models.CASCADE, primary_key=True)
    spot_price = models.ForeignKey("SpotPrice", on_delete=models.SET_NULL, null=True)
    grid_price = models.ForeignKey("GridPrice", on_delete=models.SET_NULL, null=True)

    energy = models.DecimalField(_("Energy [kWh]"), editable=False, max_digits=8, decimal_places=6)
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"), editable=False)
    price_area = models.IntegerField(_("Price area"), editable=False)
    spot_nok_pr_kwh = models.DecimalField(_("Spot price per kWh [NOK/kWh]"), editable=False, max_digits=10, decimal_places=7)
    grid_nok_pr_kwh = models.DecimalField(_("Grid price per kWh [NOK/kWh]"), editable=False, max_digits=10, decimal_places=7)

    spot_cost = models.DecimalField(_("Spot cost [NOK]"), editable=False, max_digits=11, decimal_places=7)
    grid_cost = models.DecimalField(_("Grid cost [NOK]"), editable=False, max_digits=11, decimal_places=7)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def set_energy(self) -> None:
        self.energy = self.energy_detail.energy

    def set_timestamp(self) -> None:
        self.timestamp = self.energy_detail.timestamp

    def set_price_area(self) -> None:
        self.price_area = self.energy_detail.charging_session.price_area

    def set_spot_price(self) -> None:
        self.spot_nok_pr_kwh = self.spot_price.nok_pr_kwh

    def set_grid_price(self) -> None:
        self.grid_nok_pr_kwh = self.grid_price.get_price(self.timestamp)

    def set_spot_cost(self) -> None:
        self.spot_cost = self.energy * self.spot_nok_pr_kwh

    def set_grid_cost(self) -> None:
        self.grid_cost = self.energy * self.grid_nok_pr_kwh

    def save(self, *args, **kwargs):
        self.set_energy()
        self.set_timestamp()
        self.set_spot_price()
        self.set_price_area()
        self.set_grid_price()
        self.set_spot_cost()
        self.set_grid_cost()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.energy_detail.id)

    class Meta:
        db_table = "costs"
        verbose_name = _("Costs")
        verbose_name_plural = _("Costs")

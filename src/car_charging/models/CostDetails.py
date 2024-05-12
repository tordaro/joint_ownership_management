from django.db import models
from django.utils.translation import gettext_lazy as _


class CostDetails(models.Model):
    energy_detail = models.OneToOneField("EnergyDetails", on_delete=models.CASCADE, primary_key=True)
    spot_price = models.ForeignKey("SpotPrice", on_delete=models.SET_NULL, null=True)
    grid_price = models.ForeignKey("GridPrice", on_delete=models.SET_NULL, null=True)

    energy = models.DecimalField(_("Energy [kWh]"), editable=False, max_digits=8, decimal_places=6)
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"), editable=False)
    price_area = models.IntegerField(_("Price area"), editable=False)
    spot_price_nok = models.DecimalField(_("Spot price per kWh [NOK/kWh]"), editable=False, max_digits=10, decimal_places=7)
    grid_price_nok = models.DecimalField(_("Grid price per kWh [NOK/kWh]"), editable=False, max_digits=10, decimal_places=7)
    user_full_name = models.CharField(verbose_name=_("User Full Name"), editable=False, max_length=100, blank=True)
    user_id = models.UUIDField(_("User ID"), editable=False, blank=True, null=True)

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
        self.spot_price_nok = self.spot_price.nok_pr_kwh

    def set_grid_price(self) -> None:
        self.grid_price_nok = self.grid_price.get_price(self.timestamp)

    def set_spot_cost(self) -> None:
        self.spot_cost = self.energy * self.spot_price_nok

    def set_grid_cost(self) -> None:
        self.grid_cost = self.energy * self.grid_price_nok

    def set_user(self) -> None:
        self.user_id = self.energy_detail.charging_session.user_id
        self.user_full_name = self.energy_detail.charging_session.user_full_name

    def save(self, *args, **kwargs):
        self.set_energy()
        self.set_timestamp()
        self.set_spot_price()
        self.set_price_area()
        self.set_grid_price()
        self.set_spot_cost()
        self.set_grid_cost()
        self.set_user()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.energy_detail.id)

    class Meta:
        db_table = "cost_details"
        verbose_name = _("Cost detail")
        verbose_name_plural = _("Cost details")

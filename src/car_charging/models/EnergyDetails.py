from django.db import models
from django.utils.translation import gettext_lazy as _

class EnergyDetails(models.Model):
    charging_session = models.ForeignKey('ChargingSession', on_delete=models.CASCADE)
    energy = models.DecimalField(max_digits=8, decimal_places=6, verbose_name=_("Energy"))
    timestamp = models.DateTimeField(verbose_name=_("Timestamp"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'energy_details'
        ordering = ['timestamp']
        verbose_name = _('Energy Detail')
        verbose_name_plural = _('Energy Details')
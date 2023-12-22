from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ZaptecToken(models.Model):
    token = models.TextField(verbose_name=_("Token"))
    token_type = models.CharField(max_length=100, blank=True, verbose_name=_("Token Type"))
    expires_in = models.IntegerField(blank=True, null=True, verbose_name=_("Time to expire [s]"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def is_token_expired(self) -> bool | None:
        if not self.expires_in:
            return None

        return self.created_at + timezone.timedelta(seconds=self.expires_in) < timezone.now()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "zaptec_token"
        ordering = ["-created_at"]
        verbose_name = _("Zaptec Token")
        verbose_name_plural = _("Zaptec Tokens")

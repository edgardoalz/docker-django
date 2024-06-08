from django.db import models
from django.utils.translation import gettext_lazy as _

from multitenant.models.tenant_model import TenantModel


class CreditType(TenantModel, models.Model):
    name = models.CharField(_("Name"), max_length=255)

    contains_public_data = True

    class Meta:
        verbose_name = _("Credit type")
        verbose_name_plural = _("Credit types")

        unique_together = (("tenant", "name"),)

    def __str__(self) -> str:
        return self.name

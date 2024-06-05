from django.db import models
from django.utils.translation import gettext_lazy as _

from company.models import Company
from multitenant.models.tenant_model import TenantModel


class Ticket(TenantModel):
    code = models.CharField(max_length=255)
    concept = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=19, decimal_places=4)
    client = models.ForeignKey(Company, models.PROTECT)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        unique_together = (("tenant", "client", "code"),)

    def __str__(self) -> str:
        return f"{self.code} - {self.total}"

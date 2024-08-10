from django.db import models
from django.utils.translation import gettext_lazy as _

from company.models import Company
from multitenant.models.tenant_model import TenantModel

from .sat_payment_method import SatPaymentMethod


class Invoice(TenantModel):
    date = models.DateField()
    due_date = models.DateField()
    code = models.CharField(max_length=255)
    concept = models.CharField(max_length=255)
    subtotal = models.DecimalField(max_digits=19, decimal_places=4)
    iva = models.DecimalField(max_digits=19, decimal_places=4)
    total = models.DecimalField(max_digits=19, decimal_places=4)
    client = models.ForeignKey(Company, models.PROTECT)
    payment_method = models.ForeignKey(SatPaymentMethod, models.PROTECT)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        unique_together = (("tenant", "client", "code"),)

    def __str__(self) -> str:
        return f"{self.date.isoformat()} - {self.code} - {self.total}"

from django.db import models
from django.utils.translation import gettext_lazy as _

from multitenant.models.tenant_model import TenantModel

from .company_type import CompanyType


class Company(TenantModel, models.Model):
    name = models.CharField(_("Name"), max_length=255)
    rfc = models.CharField("RFC", max_length=13, blank=True, null=True)
    business_name = models.CharField(
        _("Business name"),
        max_length=255,
        blank=True,
        null=True,
    )
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=10)
    contact = models.CharField(_("Contact"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    company_types = models.ManyToManyField(CompanyType, verbose_name=_("Company types"))

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

        unique_together = (("tenant", "rfc"),)

    def __str__(self):
        if self.rfc:
            return f"{self.name} - RFC: {self.rfc}"
        return self.name

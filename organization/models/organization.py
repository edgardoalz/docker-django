from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from account.models.account import Account
from multitenant.models.tenant_model import TenantModel


class Organization(TenantModel, models.Model):
    name = models.CharField(_("Name"), max_length=255)
    rfc = models.CharField("RFC", max_length=13, blank=True, null=True)
    business_name = models.CharField(
        _("Business name"), max_length=255, blank=True, null=True
    )
    account = models.OneToOneField(Account, models.CASCADE, verbose_name=_("Account"))

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

        unique_together = (("tenant", "rfc"),)

    def soft_delete(self):
        with transaction.atomic():
            self.account.soft_delete()
            super().soft_delete()

    def __str__(self):
        if self.rfc:
            return f"{self.name} - RFC: {self.rfc}"
        return self.name

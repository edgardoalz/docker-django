from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from account.models.account import Account
from multitenant.models.tenant_model import TenantModel

from ..constants import BankAccountType
from .bank import Bank


class BankAccount(TenantModel):
    account_number = models.CharField(_("Account number"), max_length=24)
    name = models.CharField(_("Name"), max_length=255)
    owner_name = models.CharField(_("Owner name"), max_length=255)
    type = models.CharField(_("Type"), choices=BankAccountType.choices, max_length=20)
    bank = models.ForeignKey(Bank, models.PROTECT, verbose_name=_("Bank"))
    account = models.OneToOneField(Account, models.CASCADE, verbose_name=_("Account"))

    class Meta:
        verbose_name = _("Bank account")
        verbose_name_plural = _("Bank accounts")

    def soft_delete(self) -> None:
        with transaction.atomic():
            self.account.soft_delete()
            super().soft_delete()

    def __str__(self) -> str:
        return self.name

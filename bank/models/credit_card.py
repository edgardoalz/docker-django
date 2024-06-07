from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from account.models.account import Account
from common.models.clean_on_save import CleanOnSaveMixin
from multitenant.models.tenant_model import TenantModel

from .bank import Bank


class CreditCard(TenantModel, CleanOnSaveMixin, models.Model):
    account_number = models.CharField(_("Account number"), max_length=4)
    name = models.CharField(_("Name"), max_length=255)
    owner_name = models.CharField(_("Owner name"), max_length=255)
    closing_day = models.PositiveIntegerField(
        _("Closing day"), validators=[MinValueValidator(1), MaxValueValidator(28)]
    )
    payment_due_day = models.PositiveIntegerField(
        _("Payment due day"), validators=[MinValueValidator(1), MaxValueValidator(28)]
    )
    credit_limit = models.PositiveIntegerField(_("Credit limit"))
    bank = models.ForeignKey(Bank, models.PROTECT, verbose_name=_("Bank"))
    account = models.OneToOneField(Account, models.CASCADE, verbose_name=_("Account"))

    class Meta:
        verbose_name = _("Credit card")
        verbose_name_plural = _("Credit cards")

    def soft_delete(self) -> None:
        with transaction.atomic():
            self.account.soft_delete()
            super().soft_delete()

    def __str__(self) -> str:
        return self.name

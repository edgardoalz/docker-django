from decimal import Decimal

from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from common.models.clean_on_save import CleanOnSaveMixin
from multitenant.models.tenant_model import TenantModel

from ..constants import AccountMoveType
from .account import Account


class AccountMove(TenantModel, CleanOnSaveMixin, models.Model):
    date = models.DateField(_("Date"))
    type = models.CharField(_("Type"), choices=AccountMoveType.choices, max_length=10)
    notes = models.TextField(_("Notes"), blank=True)

    initial_balance = models.DecimalField(
        _("Initial balance"), max_digits=19, decimal_places=4
    )
    amount = models.DecimalField(_("Amount"), max_digits=19, decimal_places=4)
    balance = models.DecimalField(_("Balance"), max_digits=19, decimal_places=4)

    account_id: int | None
    account = models.ForeignKey(
        Account, models.PROTECT, related_name="moves", verbose_name=_("Account")
    )

    class Meta:
        verbose_name = _("Account move")
        verbose_name_plural = _("Account moves")

    def save(self, *args, **kargs) -> None:
        self.balance = self._calculate_balance()
        return super().save(*args, **kargs)

    def _calculate_balance(self) -> Decimal:
        if self.type == AccountMoveType.income:
            return self.initial_balance + self.amount

        return self.initial_balance - self.amount

    def __str__(self) -> str:
        result = f"{self.account.name}[{self.date.isoformat()}] "
        balance_parts = (self.initial_balance, self.amount, self.balance)
        result += " | ".join(map(str, balance_parts))
        type_label = AccountMoveType(self.type).label
        result += f" | {gettext(type_label)}"
        return result

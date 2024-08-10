from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta

from multitenant.models.tenant_model import TenantModel

if TYPE_CHECKING:
    from .account_move import AccountMove


class Account(TenantModel, models.Model):
    name = models.CharField(max_length=255)
    initial_balance = models.DecimalField(
        max_digits=19,
        decimal_places=4,
        blank=True,
    )
    balance = models.DecimalField(
        max_digits=19,
        decimal_places=4,
    )

    moves: models.Manager["AccountMove"]

    class Meta(TypedModelMeta):
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kargs) -> None:
        if self.initial_balance is None:
            self.initial_balance = self.balance
        super().save(*args, **kargs)

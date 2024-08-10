from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from common.admin.base import BaseModelAdmin
from multitenant.admin import TenantModelAdmin

from .models.bank import Bank
from .models.bank_account import BankAccount
from .models.credit_card import CreditCard


@admin.register(Bank)
class BankAdmin(BaseModelAdmin[Bank], admin.ModelAdmin[Bank]):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(BankAccount)
class BankAccountAdmin(TenantModelAdmin[BankAccount]):
    list_display = ["name", "account_number", "balance"]
    search_fields = ["name", "account_number"]

    @admin.display(description=_("Balance"), ordering="account__balance")
    def balance(self, obj: BankAccount):
        return "$%s" % obj.account.balance


@admin.register(CreditCard)
class CreditCardAdmin(TenantModelAdmin[CreditCard]):
    list_display = ["name", "account_number", "balance"]
    search_fields = ["name", "account_number"]

    @admin.display(description=_("Balance"), ordering="account__balance")
    def balance(self, obj: CreditCard):
        return "$%s" % obj.account.balance

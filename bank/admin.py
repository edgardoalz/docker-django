from django.contrib import admin

from common.admin.base import BaseModelAdmin
from multitenant.admin import TenantModelAdmin

from .models.bank import Bank
from .models.bank_account import BankAccount


# Register your models here.
@admin.register(Bank)
class BankAdmin(BaseModelAdmin[Bank], admin.ModelAdmin[Bank]):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(BankAccount)
class BankAccountAdmin(TenantModelAdmin[BankAccount]):
    list_display = ["name", "account_number", "balance"]
    search_fields = ["name", "account_number"]

    @admin.display(description="Balance", ordering="account__balance")
    def balance(self, obj: BankAccount):
        return "$%s" % obj.account.balance

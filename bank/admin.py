from django.contrib import admin

from common.admin.base import BaseModelAdmin

from .models.bank import Bank


# Register your models here.
@admin.register(Bank)
class BankAdmin(BaseModelAdmin[Bank], admin.ModelAdmin[Bank]):
    list_display = ["name"]
    search_fields = ["name"]

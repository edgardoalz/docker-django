from django.contrib import admin

from multitenant.admin import TenantModelAdmin

from .models.credit_type import CreditType


@admin.register(CreditType)
class CreditTypeAdmin(TenantModelAdmin[CreditType]):
    list_display = ("name",)
    search_fields = ("name",)

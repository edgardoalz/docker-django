from django.contrib import admin

from common.admin.base import BaseModelAdmin

from .models.tenant import Tenant


@admin.register(Tenant)
class TenantAdmin(BaseModelAdmin[Tenant], admin.ModelAdmin[Tenant]):
    list_display = ["name"]
    search_fields = ["name"]

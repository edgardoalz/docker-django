from django.contrib import admin

from multitenant.admin import TenantModelAdmin

from .models.company import Company


@admin.register(Company)
class CompanyAdmin(TenantModelAdmin[Company], admin.ModelAdmin[Company]):
    list_display = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("company_types",)

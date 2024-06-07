from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from multitenant.admin import TenantModelAdmin

from .models.organization import Organization


@admin.register(Organization)
class OrganizationAdmin(TenantModelAdmin[Organization]):
    list_display = ("name", "rfc", "balance")
    search_fields = ("name", "rfc")

    @admin.display(description=_("Balance"), ordering="account__balance")
    def balance(self, obj: Organization):
        return "$%s" % obj.account.balance

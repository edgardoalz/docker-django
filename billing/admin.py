from django.contrib import admin

from billing.models import Invoice, SatPaymentMethod, Ticket
from common.admin.base import BaseModelAdmin
from multitenant.admin import TenantModelAdmin


@admin.register(SatPaymentMethod)
class SatPaymentMethodAdmin(BaseModelAdmin[SatPaymentMethod]):
    list_display = ["name", "code"]
    search_fields = ["name", "code"]


@admin.register(Invoice)
class InvoiceAdmin(TenantModelAdmin[Invoice]):
    list_display = ["code", "concept", "total"]
    search_fields = ["code", "concept"]
    autocomplete_fields = ["client", "payment_method"]


@admin.register(Ticket)
class TicketAdmin(TenantModelAdmin[Ticket]):
    list_display = ["code", "concept", "total"]
    search_fields = ["code", "concept"]
    autocomplete_fields = ["client"]

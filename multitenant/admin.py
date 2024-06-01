from typing import Any, Sequence, TypeVar

from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.http import HttpRequest

from common.admin.base import BaseModelAdmin

from .models.tenant import Tenant
from .models.tenant_model import TenantModel

T = TypeVar("T", bound=TenantModel)


class TenantModelAdmin(BaseModelAdmin[T]):
    def get_readonly_fields(  # type: ignore[override]
        self, request: HttpRequest, obj: T | None = None
    ) -> Sequence[Any]:
        readonly_fields = super().get_readonly_fields(request, obj)
        return tuple(readonly_fields) + ("tenant",)

    def get_list_filter(self, request: HttpRequest) -> Sequence[Any]:  # type: ignore[override]
        list_filter = super().get_list_filter(request)
        return tuple(list_filter) + (AutocompleteFilterFactory("Tenant", "tenant"),)


@admin.register(Tenant)
class TenantAdmin(BaseModelAdmin[Tenant], admin.ModelAdmin[Tenant]):
    list_display = ["name"]
    search_fields = ["name"]

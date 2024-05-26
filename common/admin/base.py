from typing import Generic, TypeVar

from django.contrib import admin
from django.contrib.admin.options import _DisplayT, _ListFilterT
from django.http import HttpRequest
from django.utils.datastructures import _ListOrTuple

from ..models.base import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class BaseModelAdmin(admin.ModelAdmin[TModel], Generic[TModel]):
    list_per_page = 15

    def get_readonly_fields(
        self, request: HttpRequest, obj: TModel | None = None
    ) -> _ListOrTuple[str]:
        readonly_fields = super().get_readonly_fields(request, obj)
        return tuple[str](readonly_fields) + (
            "uuid",
            "created_at",
            "updated_at",
            "deleted_at",
        )

    def get_list_filter(self, request: HttpRequest) -> _ListOrTuple[_ListFilterT]:
        list_filter = super().get_list_filter(request)
        return tuple(list_filter) + ("is_active",)

    def get_list_display(self, request: HttpRequest) -> _DisplayT:
        list_display = super().get_list_display(request)
        return tuple(list_display) + ("is_active",)

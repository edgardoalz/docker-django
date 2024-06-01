from typing import Any, Generic, Sequence, TypeVar

from django.contrib.admin.options import ModelAdmin
from django.http import HttpRequest

from ..models.base import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


class BaseModelAdmin(ModelAdmin[TModel], Generic[TModel]):
    list_per_page = 15

    def get_readonly_fields(  # type: ignore[override]
        self, request: HttpRequest, obj: TModel | None = None
    ) -> Sequence[Any]:
        readonly_fields = super().get_readonly_fields(request, obj)
        return tuple[str](readonly_fields) + (
            "uuid",
            "created_at",
            "updated_at",
            "deleted_at",
        )

    def get_list_filter(self, request: HttpRequest) -> Sequence[Any]:  # type: ignore[override]
        list_filter = super().get_list_filter(request)
        return tuple(list_filter) + ("is_active",)

    def get_list_display(self, request: HttpRequest) -> Sequence[Any]:  # type: ignore[override]
        list_display = super().get_list_display(request)
        return tuple(list_display) + ("is_active",)

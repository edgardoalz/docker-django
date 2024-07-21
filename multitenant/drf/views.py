from typing import TypeVar

from django.db import models
from rest_framework import generics

from ..models.tenant import Tenant
from ..models.tenant_model import TenantManager, TenantModel
from ..utils import get_tenant_from_request
from .exceptions import MissingTenant

T = TypeVar("T", bound=TenantModel)


class TenantAPIView(generics.GenericAPIView, generics.UsesQuerySet[T]):
    tenant: Tenant | None
    queryset: models.QuerySet[T]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tenant = None

    @property
    def include_public(self) -> bool:
        return self.queryset.model.contains_public_data

    def get_include_public(self) -> bool:
        return self.include_public

    def get_queryset(self) -> TenantManager:
        assert (
            self.queryset.model == TenantModel
        ), f"Model {self.queryset.model} must be a TenantModel"

        if not self.tenant:
            raise MissingTenant

        include_public = self.get_include_public()
        return self.queryset.model.tenant_set.with_tenant(
            tenant_id=self.tenant.pk, include_public=include_public
        )

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        if not self.tenant:
            self.tenant = get_tenant_from_request(request)

        if not self.tenant:
            raise MissingTenant

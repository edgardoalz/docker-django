from typing import Generic, TypeVar

from rest_framework import mixins
from rest_framework.viewsets import ViewSetMixin

from ..models.tenant_model import TenantModel
from .permissions import TenantModelPermission
from .views import TenantAPIView

T = TypeVar("T", bound=TenantModel)


class TenantGenericViewSet(ViewSetMixin, TenantAPIView[T], Generic[T]):
    def get_permissions(self):
        permissions = super().get_permissions()
        permissions + [TenantModelPermission()]
        return permissions

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["tenant"] = self.tenant
        return context


class TenantReadOnlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    TenantGenericViewSet[T],
    Generic[T],
):
    pass


class TenantModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    TenantGenericViewSet[T],
    Generic[T],
):
    pass

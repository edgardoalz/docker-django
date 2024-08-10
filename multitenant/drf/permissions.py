import logging

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from ..models.tenant_model import TenantModel
from .views import TenantAPIView

logger = logging.getLogger("TenantModelPermission")


class TenantModelPermission(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: TenantModel):
        if obj.is_public:
            return request.method in SAFE_METHODS

        assert isinstance(view, TenantAPIView), f"View {view} must be a TenantAPIView"

        # Non public objects require a tenant
        if not view.tenant:
            obj_tag = f"{obj.__class__.__name__} {obj.pk}"
            logger.warn(
                "Tenant Permission evaluated without tenant for",
                extra={"object": obj_tag},
            )
            return False

        return obj.tenant_id == view.tenant.pk

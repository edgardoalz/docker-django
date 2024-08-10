import logging

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from finance_auth.models import User

from .constants import TENANT_HEADER_KEY
from .models import Tenant

logger = logging.getLogger(__name__)


def get_tenant_uuid_from_request(request: HttpRequest):
    return request.headers.get(TENANT_HEADER_KEY)


def get_tenant_from_request(request: HttpRequest):
    if isinstance(request.user, AnonymousUser):
        return None

    tenant_uuid = get_tenant_uuid_from_request(request)

    if tenant_uuid is None:
        return None

    try:
        user: User = request.user
        tenant = user.tenants.get(uuid=tenant_uuid)
        return tenant
    except Tenant.DoesNotExist:
        logger.warn(
            "Tenant not found for user",
            extra={"tenant_uuid": tenant_uuid, "user": user.uuid},
        )
        return None

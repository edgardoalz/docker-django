from rest_framework.request import Request

from ..models.tenant import Tenant


class RequestWithTenant(Request):
    tenant: Tenant | None = None

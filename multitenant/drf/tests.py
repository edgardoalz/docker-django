from rest_framework.test import APIClient, APITestCase

from finance_auth.factories.user import UserFactory
from finance_auth.models.user import User

from ..constants import TENANT_HEADER_KEY
from ..factories.tenant import TenantFactory
from ..models import Tenant


class TenantAPIClient(APIClient):
    def setTenant(self, tenant: Tenant):
        self.tenant = tenant

    def request(self, **kwargs):
        if self.tenant:
            kwargs[f"HTTP_{TENANT_HEADER_KEY}"] = self.tenant.uuid
        return super().request(**kwargs)


class TenantApiTestCase(APITestCase):
    client: TenantAPIClient
    client_class = TenantAPIClient

    def setUpUser(self, user: User | None = None, tenant: Tenant | None = None):
        """
        Create a user and tenant and set the tenant in the client.
        """
        self.user = user or UserFactory()
        self.tenant = tenant or TenantFactory()
        self.client.setTenant(self.tenant)
        self.user.tenants.add(self.tenant)

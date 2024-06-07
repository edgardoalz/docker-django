from django.test import TestCase

from account.models.account import Account
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ...factories.organization import OrganizationFactory
from ..organization import Organization


class OrganizationTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        organization = OrganizationFactory(name="Test", rfc="XXXX123456XXX")
        self.assertEqual(str(organization), "Test - RFC: XXXX123456XXX")

        organization.rfc = None
        organization.save()
        self.assertEqual(str(organization), "Test")

    def test_retrieve_tenant_companies(self):
        tenant_companies = [
            OrganizationFactory(tenant=self.tenant),
            OrganizationFactory(tenant=self.tenant),
        ]
        OrganizationFactory()

        tenant_companies_lookup = Organization.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_companies_lookup), 2)
        for organization in tenant_companies:
            self.assertIn(organization, tenant_companies_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            OrganizationFactory(tenant=None)

    def test_soft_delete(self):
        organization = OrganizationFactory()
        organization.soft_delete()
        self.assertFalse(Organization.objects.filter(pk=organization.pk).exists())
        self.assertTrue(
            Organization.objects.deleted().filter(pk=organization.pk).exists()
        )
        self.assertFalse(Account.objects.filter(pk=organization.account.pk).exists())
        self.assertTrue(
            Account.objects.deleted().filter(pk=organization.account.pk).exists()
        )

from django.test import TestCase

from multitenant.factories.tenant import TenantFactory

from ...factories.company import CompanyFactory
from ..company import Company


class CompanyTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        company = CompanyFactory(name="Test", rfc="XXXX123456XXX")
        self.assertEqual(str(company), "Test - RFC: XXXX123456XXX")

        company.rfc = None
        company.save()
        self.assertEqual(str(company), "Test")

    def test_retrieve_tenant_companies(self):
        tenant_companies = [
            CompanyFactory(tenant=self.tenant),
            CompanyFactory(tenant=self.tenant),
        ]
        CompanyFactory()

        tenant_companies_lookup = Company.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_companies_lookup), 2)
        for company in tenant_companies:
            self.assertIn(company, tenant_companies_lookup)

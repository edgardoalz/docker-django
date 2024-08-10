from datetime import date
from decimal import Decimal

from django.test import TestCase

from billing.factories.invoice import InvoiceFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ..invoice import Invoice


class InvoiceTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        invoice = InvoiceFactory(
            date=date(2024, 6, 5), code="CFDI-123", total=Decimal("100.00")
        )
        self.assertEqual(str(invoice), "2024-06-05 - CFDI-123 - 100.00")

    def test_retrieve_tenant_invoices(self):
        tenant_invoices = [
            InvoiceFactory(tenant=self.tenant),
            InvoiceFactory(tenant=self.tenant),
        ]
        InvoiceFactory()

        tenant_invoices_lookup = Invoice.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_invoices_lookup), 2)
        for invoice in tenant_invoices:
            self.assertIn(invoice, tenant_invoices_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            InvoiceFactory(tenant=None)

    def test_soft_delete(self):
        invoice = InvoiceFactory()
        invoice.soft_delete()
        self.assertFalse(Invoice.objects.filter(pk=invoice.pk).exists())
        self.assertTrue(Invoice.objects.deleted().filter(pk=invoice.pk).exists())

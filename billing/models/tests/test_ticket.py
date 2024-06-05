from decimal import Decimal

from django.test import TestCase

from billing.factories.ticket import TicketFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ..ticket import Ticket


class TicketTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        ticket = TicketFactory(code="CFDI-123", total=Decimal("100.00"))
        self.assertEqual(str(ticket), "CFDI-123 - 100.00")

    def test_retrieve_tenant_tickets(self):
        tenant_tickets = [
            TicketFactory(tenant=self.tenant),
            TicketFactory(tenant=self.tenant),
        ]
        TicketFactory()

        tenant_tickets_lookup = Ticket.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_tickets_lookup), 2)
        for ticket in tenant_tickets:
            self.assertIn(ticket, tenant_tickets_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            TicketFactory(tenant=None)

    def test_soft_delete(self):
        ticket = TicketFactory()
        ticket.soft_delete()
        self.assertFalse(Ticket.objects.filter(pk=ticket.pk).exists())
        self.assertTrue(Ticket.objects.deleted().filter(pk=ticket.pk).exists())

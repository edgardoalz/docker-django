from decimal import Decimal

from django.test import TestCase

from account.factories.account import AccountFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ..account import Account


class AccountTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        account = AccountFactory(name="Cuenta de banco", balance=Decimal("0.00"))
        self.assertEqual(str(account), "Cuenta de banco")

    def test_initial_balance(self):
        account = AccountFactory(name="Cuenta de banco", balance=Decimal("100.00"))
        self.assertEqual(
            Account.objects.get(pk=account.pk).initial_balance, Decimal("100.00")
        )

    def test_initial_balance_only_set_once(self):
        # Balance of 0 should be considered as correct initial balance
        account = AccountFactory(name="Cuenta de banco", balance=Decimal("0"))
        account.balance = Decimal("100.00")
        account.save()
        self.assertEqual(
            Account.objects.get(pk=account.pk).initial_balance, Decimal("0.00")
        )

    def test_retrieve_tenant_accounts(self):
        tenant_accounts = [
            AccountFactory(tenant=self.tenant),
            AccountFactory(tenant=self.tenant),
        ]
        AccountFactory()

        tenant_accounts_lookup = Account.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_accounts_lookup), 2)
        for account in tenant_accounts:
            self.assertIn(account, tenant_accounts_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            AccountFactory(tenant=None)

    def test_soft_delete(self):
        account = AccountFactory()
        account.soft_delete()
        self.assertFalse(Account.objects.filter(pk=account.pk).exists())
        self.assertTrue(Account.objects.deleted().filter(pk=account.pk).exists())

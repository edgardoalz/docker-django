from django.test import TestCase

from account.models.account import Account
from bank.factories.bank_account import BankAccountFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ..bank_account import BankAccount


class BankAccountTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        bank_account = BankAccountFactory(name="BBVA Blue")
        self.assertEqual(str(bank_account), "BBVA Blue")

    def test_retrieve_tenant_bank_accounts(self):
        tenant_bank_accounts = [
            BankAccountFactory(tenant=self.tenant),
            BankAccountFactory(tenant=self.tenant),
        ]
        BankAccountFactory()

        tenant_bank_accounts_lookup = BankAccount.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_bank_accounts_lookup), 2)
        for bank_account in tenant_bank_accounts:
            self.assertIn(bank_account, tenant_bank_accounts_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            BankAccountFactory(tenant=None)

    def test_soft_delete(self):
        bank_account = BankAccountFactory()
        bank_account.soft_delete()
        self.assertFalse(BankAccount.objects.filter(pk=bank_account.pk).exists())
        self.assertTrue(
            BankAccount.objects.deleted().filter(pk=bank_account.pk).exists()
        )

        self.assertFalse(Account.objects.filter(pk=bank_account.account.pk).exists())
        self.assertTrue(
            Account.objects.deleted().filter(pk=bank_account.account.pk).exists()
        )

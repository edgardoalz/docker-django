from django.db.utils import IntegrityError
from django.test import TestCase

from ..bank import Bank


class BankTestCase(TestCase):
    def test_str(self):
        bank = Bank.objects.create(code="american_express", name="American Express")
        self.assertEqual(str(bank), "Bank[american_express]: American Express")

    def test_code_unique(self):
        Bank.objects.create(code="american_express", name="American Express")
        with self.assertRaisesMessage(
            IntegrityError,
            "Duplicate entry 'american_express' for key 'bank_bank.code'",
        ):
            Bank.objects.create(code="american_express", name="American Express")

    def test_soft_delete(self):
        bank = Bank.objects.create(code="american_express", name="American Express")
        bank.soft_delete()
        self.assertFalse(Bank.objects.filter(code="american_express").exists())
        self.assertTrue(Bank.objects.deleted().filter(code="american_express").exists())

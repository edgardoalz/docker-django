from django.core.exceptions import ValidationError
from django.db.models.fields import Field
from django.test import TestCase

from ...constants import BankCodes
from ..bank import Bank


class BankTestCase(TestCase):
    def test_bank_str(self):
        bank = Bank.objects.get(code=BankCodes.american_express)
        self.assertEqual(str(bank), f"Bank: {bank.name}")

    def test_create_invalid_code(self):
        error_message = Field().error_messages["invalid_choice"] % dict(value="Test")
        with self.assertRaisesMessage(ValidationError, error_message):
            Bank.objects.create(code="Test", name="Test")

    def test_create_derives_name_from_code(self):
        # We can't create a bank with the same code, so we delete the existing one
        Bank.objects.filter(code=BankCodes.american_express).delete()

        bank = Bank.objects.create(code=BankCodes.american_express, name="Test")
        self.assertEqual(bank.name, BankCodes.american_express.label)

    def test_update_invalid_code(self):
        bank = Bank.objects.get(code=BankCodes.american_express)
        bank.code = "Test"

        error_message = Field().error_messages["invalid_choice"] % dict(value="Test")
        with self.assertRaisesMessage(ValidationError, error_message):
            bank.save()

    def test_update_name_ignored_deriving_from_code(self):
        bank = Bank.objects.get(code=BankCodes.american_express)
        bank.name = "Test"
        bank.save()
        self.assertEqual(bank.name, BankCodes.american_express.label)

    def test_bank_codes_exist(self):
        banks = Bank.objects.all()
        self.assertEqual(len(banks), len(BankCodes.values))
        for bank in banks:
            self.assertIn(bank.code, BankCodes.values)

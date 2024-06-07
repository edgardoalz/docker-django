from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.test import TestCase

from account.models.account import Account
from bank.factories.credit_card import CreditCardFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ..credit_card import CreditCard


class CreditCardTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        credit_card = CreditCardFactory(name="BBVA Blue")
        self.assertEqual(str(credit_card), "BBVA Blue")

    def test_retrieve_tenant_credit_cards(self):
        tenant_credit_cards = [
            CreditCardFactory(tenant=self.tenant),
            CreditCardFactory(tenant=self.tenant),
        ]
        CreditCardFactory()

        tenant_credit_cards_lookup = CreditCard.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_credit_cards_lookup), 2)
        for credit_card in tenant_credit_cards:
            self.assertIn(credit_card, tenant_credit_cards_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            CreditCardFactory(tenant=None)

    def test_soft_delete(self):
        credit_card = CreditCardFactory()
        credit_card.soft_delete()
        self.assertFalse(CreditCard.objects.filter(pk=credit_card.pk).exists())
        self.assertTrue(CreditCard.objects.deleted().filter(pk=credit_card.pk).exists())

        self.assertFalse(Account.objects.filter(pk=credit_card.account.pk).exists())
        self.assertTrue(
            Account.objects.deleted().filter(pk=credit_card.account.pk).exists()
        )

    def test_closing_day_validation(self):
        with self.assertRaisesMessage(
            ValidationError, MinValueValidator(1).message % {"limit_value": 1}
        ):
            CreditCardFactory(closing_day=0)

        with self.assertRaisesMessage(
            ValidationError, MaxValueValidator(28).message % {"limit_value": 28}
        ):
            CreditCardFactory(closing_day=29)

    def test_payment_due_day_validation(self):
        with self.assertRaisesMessage(
            ValidationError, MinValueValidator(1).message % {"limit_value": 1}
        ):
            CreditCardFactory(payment_due_day=0)

        with self.assertRaisesMessage(
            ValidationError, MaxValueValidator(28).message % {"limit_value": 28}
        ):
            CreditCardFactory(payment_due_day=29)

from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Field
from django.test import TestCase

from account.factories.account_move import AccountMoveFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import MissingTenantError

from ...constants import AccountMoveType
from ..account_move import AccountMove


class AccountMoveTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        account_move = AccountMoveFactory(
            date=date(2024, 6, 1),
            type=AccountMoveType.income,
            initial_balance=Decimal("100.00"),
            amount=Decimal("50.00"),
            balance=Decimal("150.00"),
            notes="Cuenta de banco",
            account__name="Test Account",
        )
        self.assertEqual(
            str(account_move),
            f"Test Account[2024-06-01] 100.00 | 50.00 | 150.00 | {AccountMoveType.income.label}",
        )

    def test_balance_calculation(self):
        account_move = AccountMoveFactory(
            type=AccountMoveType.income,
            initial_balance=Decimal("100.00"),
            amount=Decimal("50.00"),
        )
        self.assertEqual(account_move.balance, Decimal("150.00"))

        account_move = AccountMoveFactory(
            type=AccountMoveType.outcome,
            initial_balance=Decimal("100.00"),
            amount=Decimal("50.00"),
        )
        self.assertEqual(account_move.balance, Decimal("50.00"))

    def test_invalid_type(self):
        error_message = Field().error_messages["invalid_choice"] % {"value": "invalid"}
        with self.assertRaisesMessage(ValidationError, error_message):
            AccountMoveFactory(type="invalid")

    def test_retrieve_tenant_account_moves(self):
        tenant_account_moves = [
            AccountMoveFactory(tenant=self.tenant),
            AccountMoveFactory(tenant=self.tenant),
        ]
        AccountMoveFactory()

        tenant_account_moves_lookup = AccountMove.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_account_moves_lookup), 2)
        for account_move in tenant_account_moves:
            self.assertIn(account_move, tenant_account_moves_lookup)

    def test_tenant_required(self):
        with self.assertRaises(MissingTenantError):
            AccountMoveFactory(tenant=None)

    def test_soft_delete(self):
        account_move = AccountMoveFactory()
        account_move.soft_delete()
        self.assertFalse(AccountMove.objects.filter(pk=account_move.pk).exists())
        self.assertTrue(
            AccountMove.objects.deleted().filter(pk=account_move.pk).exists()
        )

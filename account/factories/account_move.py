from decimal import Decimal

import factory

from account.factories.account import AccountFactory
from multitenant.factories.tenant import TenantFactory

from ..constants import AccountMoveType
from ..models.account_move import AccountMove


class AccountMoveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccountMove

    date = factory.Faker("date")
    type = AccountMoveType.income
    notes = factory.Faker("text")

    initial_balance = Decimal("0.00")
    amount = Decimal("10.00")
    balance = Decimal("10.00")

    account_id: int | None
    account = factory.SubFactory(AccountFactory)

    tenant = factory.SubFactory(TenantFactory)

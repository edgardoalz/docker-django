from decimal import Decimal

import factory

from multitenant.factories.tenant import TenantFactory

from ..models.account import Account


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.Faker("company")
    balance = factory.LazyAttribute(lambda o: Decimal("100.00"))
    initial_balance: Decimal
    tenant = factory.SubFactory(TenantFactory)

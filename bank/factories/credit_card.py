import factory

from account.factories.account import AccountFactory
from multitenant.factories.tenant import TenantFactory

from ..models.credit_card import CreditCard
from .bank import BankFactory


class CreditCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditCard

    account_number = factory.Faker("numerify", text="####")
    name = factory.Faker("sentence")
    owner_name = factory.Faker("sentence")
    closing_day = factory.Faker("random_int", min=1, max=28)
    payment_due_day = factory.Faker("random_int", min=1, max=28)
    credit_limit = factory.Faker("random_int", min=1)
    bank = factory.SubFactory(BankFactory)
    account = factory.SubFactory(AccountFactory)
    tenant = factory.SubFactory(TenantFactory)

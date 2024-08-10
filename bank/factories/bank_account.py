import factory

from account.factories.account import AccountFactory
from multitenant.factories.tenant import TenantFactory

from ..constants import BankAccountType
from ..models.bank_account import BankAccount
from .bank import BankFactory


class BankAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankAccount

    account_number = factory.Faker("numerify", text="############")
    name = factory.Faker("sentence")
    owner_name = factory.Faker("sentence")
    type = BankAccountType.checking_account
    bank = factory.SubFactory(BankFactory)
    account = factory.SubFactory(
        AccountFactory,
        name=factory.SelfAttribute("..name"),
        tenant=factory.SelfAttribute("..tenant"),
    )
    tenant = factory.SubFactory(TenantFactory)

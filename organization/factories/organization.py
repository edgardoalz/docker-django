import factory

from account.factories.account import AccountFactory
from multitenant.factories.tenant import TenantFactory

from ..models.organization import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("company")
    rfc = factory.Faker("bothify", text="?????????????")
    business_name = factory.LazyAttribute(lambda o: o.name)
    account = factory.SubFactory(AccountFactory)
    tenant = factory.SubFactory(TenantFactory)

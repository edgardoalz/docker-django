import factory

from multitenant.factories.tenant import TenantFactory

from ..models.credit_type import CreditType


class CreditTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditType

    name = factory.Faker("sentence")
    tenant = factory.SubFactory(TenantFactory)

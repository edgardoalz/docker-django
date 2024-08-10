import factory

from ..models.tenant import Tenant


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    code = factory.Faker("uuid4")
    name = factory.Faker("company")

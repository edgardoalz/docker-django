import factory

from ..models.tenant import Tenant


def TenantFactory(**kwargs) -> Tenant:
    return _TenantFactory(**kwargs)


class _TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    code = factory.Faker("uuid4")
    name = factory.Faker("company")

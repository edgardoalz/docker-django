import factory

from multitenant.factories.tenant import TenantFactory

from ..models.company import Company
from ..models.company_type import CompanyType


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    description = factory.Faker("paragraph")
    phone = factory.Faker("numerify", text="##########")
    email = factory.Faker("email")
    rfc = factory.Faker("bothify", text="?????????????")
    business_name = factory.LazyAttribute(lambda o: o.name)
    contact = factory.Faker("email")
    tenant = factory.SubFactory(TenantFactory)

    @factory.post_generation
    def company_types(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for company_type in extracted:
                self.company_types.add(company_type)
        else:
            self.company_types.add(CompanyType.objects.first())

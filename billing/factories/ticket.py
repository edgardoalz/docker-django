from decimal import Decimal

import factory

from company.constants import CompanyTypeCodes
from company.factories.company import CompanyFactory
from company.models.company_type import CompanyType
from multitenant.factories.tenant import TenantFactory

from ..models.ticket import Ticket


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    code = factory.Faker("uuid4")
    concept = factory.Faker("sentence")
    total = factory.LazyAttribute(lambda o: Decimal("116.00"))
    client = factory.LazyAttribute(
        lambda o: CompanyFactory(
            company_types=[CompanyType.objects.get(code=CompanyTypeCodes.employee)]
        )
    )
    tenant = factory.SubFactory(TenantFactory)

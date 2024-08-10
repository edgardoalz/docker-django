from datetime import date
from decimal import Decimal

import factory

from company.constants import CompanyTypeCodes
from company.factories.company import CompanyFactory
from company.models.company_type import CompanyType
from multitenant.factories.tenant import TenantFactory

from ..models.invoice import Invoice
from .sat_payment_method import SatPaymentMethodFactory


class InvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Invoice

    date = factory.LazyAttribute(lambda o: date.today())
    due_date = factory.LazyAttribute(lambda o: date.today())
    code = factory.Faker("uuid4")
    concept = factory.Faker("sentence")
    subtotal = factory.LazyAttribute(lambda o: Decimal("100.00"))
    iva = factory.LazyAttribute(lambda o: Decimal("16.00"))
    total = factory.LazyAttribute(lambda o: Decimal("116.00"))
    client = factory.LazyAttribute(
        lambda o: CompanyFactory(
            company_types=[CompanyType.objects.get(code=CompanyTypeCodes.employee)]
        )
    )
    payment_method = factory.SubFactory(SatPaymentMethodFactory)
    tenant = factory.SubFactory(TenantFactory)

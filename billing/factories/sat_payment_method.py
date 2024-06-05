import factory

from ..models.invoice import SatPaymentMethod


class SatPaymentMethodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SatPaymentMethod

    code = factory.Faker("uuid4")
    name = factory.Faker("sentence")

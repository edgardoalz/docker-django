import factory

from ..models.bank import Bank


class BankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bank

    code = factory.Faker("uuid4")
    name = factory.Faker("company")

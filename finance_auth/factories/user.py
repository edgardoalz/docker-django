import factory
import factory.fuzzy

from ..models.user import User


def fake_email_generator(instance: User, sequence):
    return f"{instance.first_name.lower()}{instance.last_name.lower()}{sequence}@example.com"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    uuid = factory.Faker("uuid4")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttributeSequence(fake_email_generator)
    is_staff = False
    is_superuser = False

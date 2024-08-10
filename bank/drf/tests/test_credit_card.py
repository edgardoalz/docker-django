from decimal import Decimal

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from parameterized import parameterized
from rest_framework import fields, status

from bank.factories.bank import BankFactory
from bank.models.credit_card import CreditCard
from common.drf.test import CRUDAPITestCase
from finance_auth.factories.user import UserFactory
from multitenant.drf.tests import TenantApiTestCase

from ...factories.credit_card import CreditCardFactory


class CreditCardApiTest(CRUDAPITestCase, TenantApiTestCase):
    url_name = "credit_card"

    def balance_value(self, value: Decimal) -> str:
        return fields.DecimalField(max_digits=19, decimal_places=4).to_representation(
            value
        )

    def expected(self, instance: CreditCard) -> dict:
        return {
            "uuid": str(instance.uuid),
            "account_number": instance.account_number,
            "name": instance.name,
            "owner_name": instance.owner_name,
            "closing_day": instance.closing_day,
            "payment_due_day": instance.payment_due_day,
            "credit_limit": instance.credit_limit,
            "bank": {
                "uuid": str(instance.bank.uuid),
                "name": instance.bank.name,
            },
            "account": {
                "uuid": str(instance.account.uuid),
                "name": instance.account.name,
                "balance": self.balance_value(instance.account.balance),
                "initial_balance": self.balance_value(instance.account.initial_balance),
            },
        }


class CreditCardListApiTest(CreditCardApiTest):
    def setUp(self):
        self.setUpUser()
        self.instances = [
            CreditCardFactory(name="Account 1", tenant=self.tenant),
            CreditCardFactory(name="Account 2", tenant=self.tenant),
        ]

    def expected_list(self):
        return [self.expected(instance) for instance in self.instances]

    def test_unauthenticated_list(self):
        response = self.list()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_outside_tenant_list(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        response = self.list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_list_result(self):
        self.client.force_authenticate(self.user)
        response = self.list()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.json(), self.expected_list())


class CreditCardRetrieveApiTest(CreditCardApiTest):
    def setUp(self):
        self.setUpUser()
        self.instance = CreditCardFactory(name="Account", tenant=self.tenant)

    def test_unauthenticated_retrieve(self):
        response = self.detail(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_outside_tenant_retrieve(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        response = self.detail(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_result(self):
        self.client.force_authenticate(self.user)
        response = self.detail(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertEqual(result, self.expected(self.instance))


class CreditCardCreateTest(CreditCardApiTest):
    def setUp(self):
        self.setUpUser()
        content_type = ContentType.objects.get_for_model(CreditCard)
        permissions = Permission.objects.filter(
            content_type=content_type, codename="add_creditcard"
        )
        self.user.user_permissions.set(permissions)
        self.bbva_bank = BankFactory(name="BBVA")

    def create_payload(self):
        return {
            "account_number": "1234",
            "name": "Account",
            "owner_name": "Owner",
            "initial_balance": "100.00",
            "closing_day": 1,
            "payment_due_day": 10,
            "credit_limit": 5000,
            "bank": str(self.bbva_bank.uuid),
        }

    def test_unauthenticated_create(self):
        response = self.create({})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(CreditCard.objects.count(), 0)

    def test_user_outside_tenant_create(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        data = self.create_payload()
        response = self.create(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(CreditCard.objects.count(), 0)

    def test_user_without_permission_create(self):
        user = UserFactory(tenants=[self.tenant])
        self.client.force_authenticate(user)
        data = self.create_payload()
        response = self.create(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(CreditCard.objects.count(), 0)

    def test_create(self):
        self.client.force_authenticate(self.user)
        data = self.create_payload()
        response = self.create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = CreditCard.objects.get(account_number=data["account_number"])
        self.assertEqual(created.name, created.account.name)
        self.assertEqual(created.tenant, created.account.tenant)
        self.assertEqual(created.account.balance, Decimal(data["initial_balance"]))
        self.assertEqual(str(created.bank.uuid), data["bank"])
        self.assertEqual(response.json(), self.expected(created))


class CreditCardUpdateTest(CreditCardApiTest):
    def setUp(self):
        self.setUpUser()
        content_type = ContentType.objects.get_for_model(CreditCard)
        permissions = Permission.objects.filter(
            content_type=content_type, codename="change_creditcard"
        )
        self.user.user_permissions.set(permissions)
        self.bbva_bank = BankFactory(name="BBVA")
        self.instance = CreditCardFactory(tenant=self.tenant)

    def test_unauthenticated_update(self):
        current_name = self.instance.name
        response = self.update(
            self.instance.uuid,
            {
                "name": "New Name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, current_name)

    def test_user_outside_tenant_update(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        current_name = self.instance.name
        response = self.update(
            self.instance.uuid,
            {
                "name": "New Name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, current_name)

    def test_user_without_permission_update(self):
        user = UserFactory(tenants=[self.tenant])
        self.client.force_authenticate(user)
        current_name = self.instance.name
        response = self.update(
            self.instance.uuid,
            {
                "name": "New Name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, current_name)

    @parameterized.expand(
        [
            ("account_number", "1111"),
            ("name", "New Name"),
            ("owner_name", "New Owner"),
            ("closing_day", 10),
            ("payment_due_day", 20),
            ("credit_limit", 10000),
            ("bank", None, "bbva_bank", True),
        ]
    )
    def test_update(self, field: str, value=None, self_key="", is_related=False):
        self.client.force_authenticate(self.user)
        data = {}
        new_value = value
        if not new_value:
            new_value = getattr(self, self_key)
        if is_related:
            new_value = str(new_value.uuid)
        data[field] = new_value
        response = self.partial_update(self.instance.uuid, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.instance.refresh_from_db()
        instance_value = getattr(self.instance, field)
        if is_related:
            self.assertEqual(str(instance_value.uuid), new_value)
        else:
            self.assertEqual(instance_value, new_value)
        self.assertEqual(response.json(), self.expected(self.instance))


class CreditCardDeleteTest(CreditCardApiTest):
    def setUp(self):
        self.setUpUser()
        content_type = ContentType.objects.get_for_model(CreditCard)
        permissions = Permission.objects.filter(
            content_type=content_type, codename="delete_creditcard"
        )
        self.user.user_permissions.set(permissions)
        self.instance = CreditCardFactory(tenant=self.tenant)

    def test_unauthenticated_delete(self):
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(CreditCard.objects.filter(uuid=self.instance.uuid).exists())

    def test_user_outside_tenant_delete(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CreditCard.objects.filter(uuid=self.instance.uuid).exists())

    def test_user_without_permission_delete(self):
        user = UserFactory(tenants=[self.tenant])
        self.client.force_authenticate(user)
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CreditCard.objects.filter(uuid=self.instance.uuid).exists())

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CreditCard.objects.filter(uuid=self.instance.uuid).exists())
        self.assertTrue(
            CreditCard.objects.deleted().filter(uuid=self.instance.uuid).exists()
        )

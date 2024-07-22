from decimal import Decimal

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import fields, status

from bank.constants import BankAccountType
from bank.factories.bank import BankFactory
from bank.models.bank_account import BankAccount
from common.drf.test import CRUDAPITestCase
from finance_auth.factories.user import UserFactory
from multitenant.drf.tests import TenantApiTestCase

from ...factories.bank_account import BankAccountFactory


class BankAccountApiTest(CRUDAPITestCase, TenantApiTestCase):
    url_name = "bank_account"

    def balance_value(self, value: Decimal) -> str:
        return fields.DecimalField(max_digits=19, decimal_places=4).to_representation(
            value
        )

    def expected(self, instance: BankAccount) -> dict:
        return {
            "uuid": str(instance.uuid),
            "account_number": instance.account_number,
            "name": instance.name,
            "owner_name": instance.owner_name,
            "type": str(instance.type),
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


class BankAccountListApiTest(BankAccountApiTest):
    def setUp(self):
        self.setUpUser()
        self.instances = [
            BankAccountFactory(name="Account 1", tenant=self.tenant),
            BankAccountFactory(name="Account 2", tenant=self.tenant),
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


class BankAccountRetrieveApiTest(BankAccountApiTest):
    def setUp(self):
        self.setUpUser()
        self.instance = BankAccountFactory(name="Account", tenant=self.tenant)

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


class BankAccountCreateTest(BankAccountApiTest):
    def setUp(self):
        self.setUpUser()
        content_type = ContentType.objects.get_for_model(BankAccount)
        permissions = Permission.objects.filter(
            content_type=content_type, codename="add_bankaccount"
        )
        self.user.user_permissions.set(permissions)
        self.bbva_bank = BankFactory(name="BBVA")

    def test_unauthenticated_create(self):
        response = self.create({})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(BankAccount.objects.count(), 0)

    def test_user_outside_tenant_create(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        data = {
            "account_number": "123456789012345678901234",
            "name": "Account",
            "owner_name": "Owner",
            "type": BankAccountType.checking_account,
            "initial_balance": "100.00",
            "bank": str(self.bbva_bank.uuid),
        }
        response = self.create(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BankAccount.objects.count(), 0)

    def test_user_without_permission_create(self):
        user = UserFactory(tenants=[self.tenant])
        self.client.force_authenticate(user)
        data = {
            "account_number": "123456789012345678901234",
            "name": "Account",
            "owner_name": "Owner",
            "type": BankAccountType.checking_account,
            "initial_balance": "100.00",
            "bank": str(self.bbva_bank.uuid),
        }
        response = self.create(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(BankAccount.objects.count(), 0)

    def test_create(self):
        self.client.force_authenticate(self.user)
        data = {
            "account_number": "123456789012345678901234",
            "name": "Account",
            "owner_name": "Owner",
            "type": BankAccountType.checking_account,
            "initial_balance": "100.00",
            "bank": str(self.bbva_bank.uuid),
        }
        response = self.create(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = BankAccount.objects.get(account_number=data["account_number"])
        self.assertEqual(created.name, created.account.name)
        self.assertEqual(created.tenant, created.account.tenant)
        self.assertEqual(response.json(), self.expected(created))


class BankAccountUpdateTest(BankAccountApiTest):
    def setUp(self):
        self.setUpUser()
        content_type = ContentType.objects.get_for_model(BankAccount)
        permissions = Permission.objects.filter(
            content_type=content_type, codename="change_bankaccount"
        )
        self.user.user_permissions.set(permissions)
        self.bbva_bank = BankFactory(name="BBVA")
        self.instance = BankAccountFactory(tenant=self.tenant)

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

    def test_update(self):
        self.client.force_authenticate(self.user)
        response = self.partial_update(
            self.instance.uuid,
            {
                "name": "New Name",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.name, "New Name")
        self.assertEqual(response.json(), self.expected(self.instance))


class BankAccountDeleteTest(BankAccountApiTest):
    def setUp(self):
        self.setUpUser()
        content_type = ContentType.objects.get_for_model(BankAccount)
        permissions = Permission.objects.filter(
            content_type=content_type, codename="delete_bankaccount"
        )
        self.user.user_permissions.set(permissions)
        self.instance = BankAccountFactory(tenant=self.tenant)

    def test_unauthenticated_delete(self):
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(BankAccount.objects.filter(uuid=self.instance.uuid).exists())

    def test_user_outside_tenant_delete(self):
        user = UserFactory()
        self.client.setTenant(self.tenant)
        self.client.force_authenticate(user)
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(BankAccount.objects.filter(uuid=self.instance.uuid).exists())

    def test_user_without_permission_delete(self):
        user = UserFactory(tenants=[self.tenant])
        self.client.force_authenticate(user)
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(BankAccount.objects.filter(uuid=self.instance.uuid).exists())

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.delete(self.instance.uuid)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BankAccount.objects.filter(uuid=self.instance.uuid).exists())
        self.assertTrue(
            BankAccount.objects.deleted().filter(uuid=self.instance.uuid).exists()
        )

from rest_framework import status

from common.drf.test import CRUDAPITestCase
from finance_auth.factories.user import UserFactory

from ...factories.bank import BankFactory


class BankApiTest(CRUDAPITestCase):
    url_name = "bank"


class BankListApiTest(BankApiTest):
    EXPECTED = [
        {
            "uuid": "00000000-0000-0000-0000-000000000001",
            "name": "BBVA",
        },
        {
            "uuid": "00000000-0000-0000-0000-000000000002",
            "name": "Santander",
        },
    ]

    def setUp(self):
        self.user = UserFactory()

        for bank in self.EXPECTED:
            BankFactory(**bank)

    def test_unauthenticated_list(self):
        response = self.list()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_result(self):
        self.client.force_authenticate(self.user)

        response = self.list()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertCountEqual(response.json(), self.EXPECTED)


class BankRetrieveApiTest(BankApiTest):
    def setUp(self):
        self.user = UserFactory()
        self.bank = BankFactory(name="BBVA")

    def test_unauthenticated_retrieve(self):
        response = self.detail(self.bank.uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_result(self):
        self.client.force_authenticate(self.user)

        response = self.detail(self.bank.uuid)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = response.json()

        self.assertEqual(result["uuid"], str(self.bank.uuid))
        self.assertEqual(result["name"], self.bank.name)


class BankForbiddenActionsTest(BankApiTest):
    def setUp(self):
        self.user = UserFactory()
        self.bank = BankFactory()

    def test_unauthenticated_create(self):
        response = self.create({})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_update(self):
        response = self.update(self.bank.uuid, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_delete(self):
        response = self.delete(self.bank.uuid)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create(self):
        self.client.force_authenticate(self.user)
        response = self.create({})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        self.client.force_authenticate(self.user)
        response = self.update(self.bank.uuid, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.delete(self.bank.uuid)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

from django.db.utils import IntegrityError
from django.test import TestCase

from credit.constants import GlobalCreditType
from credit.factories.credit_type import CreditTypeFactory
from multitenant.factories.tenant import TenantFactory
from multitenant.models.tenant_model import PublicDataMutationError

from ..credit_type import CreditType


class CreditTypeTestCase(TestCase):
    def setUp(self) -> None:
        self.tenant = TenantFactory()

    def test_str(self):
        credit_type = CreditTypeFactory(name="Infonavit")
        self.assertEqual(str(credit_type), "Infonavit")

    def test_retrieve_tenant_and_public_credit_types(self):
        tenant_credit_types = [
            CreditTypeFactory(tenant=self.tenant),
            CreditTypeFactory(tenant=self.tenant),
            CreditTypeFactory(tenant=None),
        ]
        CreditTypeFactory()

        tenant_credit_types_lookup = CreditType.tenant_set.with_tenant(self.tenant.pk)
        self.assertEqual(len(tenant_credit_types_lookup), 3 + len(GlobalCreditType))
        for credit_type in tenant_credit_types:
            self.assertIn(credit_type, tenant_credit_types_lookup)

    def test_create_public(self):
        CreditTypeFactory(tenant=None)

    def test_can_not_update_public(self):
        credit_type = CreditTypeFactory(tenant=None)
        credit_type.name = "Updated"
        with self.assertRaises(PublicDataMutationError):
            credit_type.save()

    def test_can_not_soft_delete_public(self):
        credit_type = CreditTypeFactory(tenant=None)
        with self.assertRaises(PublicDataMutationError):
            credit_type.soft_delete()

    def test_soft_delete(self):
        credit_type = CreditTypeFactory()
        credit_type.soft_delete()
        self.assertFalse(CreditType.objects.filter(pk=credit_type.pk).exists())
        self.assertTrue(CreditType.objects.deleted().filter(pk=credit_type.pk).exists())

    def test_name_unique_together_tenant(self):
        CreditTypeFactory(name="Infonavit", tenant=self.tenant)
        with self.assertRaisesMessage(
            IntegrityError, "credit_credittype.credit_credittype_tenant_id_name"
        ):
            CreditTypeFactory(name="Infonavit", tenant=self.tenant)

    def test_public_types_exist(self):
        global_types = CreditType.objects.all()
        self.assertEqual(len(global_types), len(GlobalCreditType))
        for global_type in global_types:
            self.assertIn(global_type.name, GlobalCreditType)

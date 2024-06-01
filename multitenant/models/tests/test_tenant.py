from django.db.utils import IntegrityError
from django.test import TestCase

from ..tenant import Tenant


class TenantTestCase(TestCase):
    def test_str(self):
        tenant = Tenant.objects.create(code="coronado", name="Coronado Contadores")
        self.assertEqual(str(tenant), "Tenant[coronado]: Coronado Contadores")

    def test_code_unique(self):
        Tenant.objects.create(code="coronado", name="Coronado Contadores")
        with self.assertRaisesMessage(
            IntegrityError,
            "Duplicate entry 'coronado' for key 'multitenant_tenant.code'",
        ):
            Tenant.objects.create(code="coronado", name="Coronado Contadores")

    def test_soft_delete(self):
        tenant = Tenant.objects.create(code="coronado", name="Coronado Contadores")
        tenant.soft_delete()
        self.assertFalse(Tenant.objects.filter(code="coronado").exists())
        self.assertTrue(Tenant.objects.deleted().filter(code="coronado").exists())

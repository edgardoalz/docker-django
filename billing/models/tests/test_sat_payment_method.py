from django.test import TestCase

from billing.factories.sat_payment_method import SatPaymentMethodFactory

from ..sat_payment_method import SatPaymentMethod


class SatPaymentMethodTestCase(TestCase):
    def test_str(self):
        sat_payment_method = SatPaymentMethodFactory(code="123", name="Payment Method")
        self.assertEqual(str(sat_payment_method), "Payment Method[123]")

    def test_soft_delete(self):
        sat_payment_method = SatPaymentMethodFactory()
        sat_payment_method.soft_delete()
        self.assertFalse(
            SatPaymentMethod.objects.filter(pk=sat_payment_method.pk).exists()
        )
        self.assertTrue(
            SatPaymentMethod.objects.deleted().filter(pk=sat_payment_method.pk).exists()
        )

"""Tests for the models of the ``payslip`` app."""
from django.test import TestCase
from django.utils.timezone import now

from mixer.backend.django import mixer


class PaymentTestCase(TestCase):
    """Tests for the ``Payment`` model."""
    longMessage = True

    def setUp(self):
        self.payment = mixer.blend('payslip.Payment', end_date=now())

    def test_model(self):
        self.assertTrue(str(self.payment))

    def test_get_end_date_without_tz(self):
        self.assertIsNone(self.payment.get_end_date_without_tz().tzinfo, msg=(
            'Should return the end date without timezone attribute'))

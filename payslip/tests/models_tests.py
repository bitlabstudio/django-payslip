"""Tests for the models of the ``payslip`` app."""
from django.test import TestCase
from django.utils.timezone import now

from payslip.tests.factories import PaymentFactory


class PaymentTestCase(TestCase):
    """Tests for the ``Payment`` model."""
    longMessage = True

    def setUp(self):
        self.payment = PaymentFactory(end_date=now())

    def test_get_end_date_without_tz(self):
        self.assertIsNone(self.payment.get_end_date_without_tz().tzinfo, msg=(
            'Should return the end date without timezone attribute'))

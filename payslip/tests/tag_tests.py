"""Tests for the template filters and tags of the ``payslip`` app."""
from django.test import TestCase

from payslip.templatetags.payslip_tags import get_extra_field_value
from payslip.tests.factories import ExtraFieldFactory, PaymentFactory


class TemplateFilterTestCase(TestCase):
    """Tests for the template filters."""
    longMessage = True

    def setUp(self):
        self.payment = PaymentFactory()
        self.extra_field = ExtraFieldFactory()

    def test_get_extra_field_value(self):
        self.assertEqual(get_extra_field_value(
            self.extra_field.field_type, self.payment), '&nbsp;')
        self.payment.extra_fields.add(self.extra_field)
        self.assertEqual(get_extra_field_value(
            self.extra_field.field_type, self.payment), self.extra_field.value)

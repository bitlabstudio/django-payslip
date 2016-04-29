"""Tests for the template filters and tags of the ``payslip`` app."""
from django.test import TestCase

from mixer.backend.django import mixer

from ..templatetags.payslip_tags import get_extra_field_value


class TemplateFilterTestCase(TestCase):
    """Tests for the template filters."""
    longMessage = True

    def setUp(self):
        self.payment = mixer.blend('payslip.Payment')
        self.extra_field = mixer.blend('payslip.ExtraField')

    def test_get_extra_field_value(self):
        self.assertEqual(get_extra_field_value(
            self.extra_field.field_type, self.payment), '&nbsp;')
        self.payment.extra_fields.add(self.extra_field)
        self.assertEqual(get_extra_field_value(
            self.extra_field.field_type, self.payment), self.extra_field.value)

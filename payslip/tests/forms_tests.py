"""Tests for the forms of the ``payslip`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from payslip import forms
from payslip.tests.factories import ManagerFactory


class EmployeeFormTestCase(TestCase):
    """Tests for the ``EmployeeForm`` model form."""
    longMessage = True

    def test_form(self):
        manager = ManagerFactory()
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'test@example.com',
            'password': 'test',
            'retype_password': 'test',
            'title': '1',
        }
        form = forms.EmployeeForm(company=manager.company, data=data)
        self.assertFalse(form.errors)
        form.save()
        form = forms.EmployeeForm(company=manager.company, data=data)
        self.assertFalse(form.is_valid())
        data.update({'password': 'test_fail', 'email': 'test2@example.com'})
        form = forms.EmployeeForm(company=manager.company, data=data)
        self.assertFalse(form.is_valid())

    def test_generate_username(self):
        self.user = UserFactory()
        self.user.username = forms.generate_username(self.user.email)
        self.user.save()
        self.assertIsNotNone(forms.generate_username(self.user.email))

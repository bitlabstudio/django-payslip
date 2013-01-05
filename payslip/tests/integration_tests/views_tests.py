"""Tests for the views of the ``payslip`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from payslip.tests.factories import (
    CompanyFactory,
)


class DashboardViewTestCase(ViewTestMixin, TestCase):
    """Tests for the TemplateView ``DashboardView``."""
    longMessage= True

    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'payslip_dashboard'

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.is_not_callable(user=self.user)
        self.user.is_staff = True
        self.user.save()
        self.should_be_callable_when_authenticated(self.user)


class CompanyCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``CompanyCreateView``."""
    longMessage= True

    def setUp(self):
        self.user = UserFactory()
        self.user.is_staff = True
        self.user.save()

    def get_view_name(self):
        return 'payslip_company_create'

    def test_view(self):
        self.should_redirect_to_login_when_anonymous()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='POST', data={'name': 'Foo'}, user=self.user,
                         and_redirects_to=reverse('payslip_company_update',
                                                  kwargs={'pk': 1}))


class CompanyUpdateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``CompanyUpdateView``."""
    longMessage= True

    def setUp(self):
        self.user = UserFactory()
        self.user.is_staff = True
        self.user.save()
        self.company = CompanyFactory()

    def get_view_name(self):
        return 'payslip_company_update'

    def get_view_kwargs(self):
        return {'pk': self.company.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.user)


class CompanyDeleteViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``CompanyDeleteView``."""
    longMessage= True

    def setUp(self):
        self.user = UserFactory()
        self.company = CompanyFactory()

    def get_view_name(self):
        return 'payslip_company_delete'

    def get_view_kwargs(self):
        return {'pk': self.company.pk}

    def test_view(self):
        self.is_not_callable(user=self.user)
        self.user.is_staff = True
        self.user.save()
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='POST', data={'name': 'Foo'}, user=self.user,
                         and_redirects_to=reverse('payslip_dashboard'))

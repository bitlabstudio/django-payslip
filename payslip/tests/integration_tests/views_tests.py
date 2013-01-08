"""Tests for the views of the ``payslip`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from payslip.tests.factories import (
    CompanyFactory,
    EmployeeFactory,
    ExtraFieldFactory,
    ExtraFieldTypeFactory,
    ManagerFactory,
    StaffFactory,
)


class DashboardViewTestCase(ViewTestMixin, TestCase):
    """Tests for the TemplateView ``DashboardView``."""
    longMessage= True

    def setUp(self):
        self.user = UserFactory()

    def get_view_name(self):
        return 'payslip_dashboard'

    def test_view(self):
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
        self.should_be_callable_when_authenticated(self.user)
        self.is_callable(method='POST', data={'name': 'Foo'}, user=self.user,
                         and_redirects_to=reverse('payslip_dashboard'))


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


class EmployeeCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``EmployeeCreateView``."""
    longMessage= True

    def setUp(self):
        self.manager = ManagerFactory()

    def get_view_name(self):
        return 'payslip_employee_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.manager.user)
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'test@example.com',
            'password': 'test',
            'retype_password': 'test',
            'title': '1',
        }
        self.is_callable(method='POST', data=data, user=self.manager.user,
                         and_redirects_to=reverse('payslip_dashboard'))


class EmployeeUpdateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``EmployeeUpdateView``."""
    longMessage= True

    def setUp(self):
        self.manager = ManagerFactory()
        self.employee = EmployeeFactory(company=self.manager.company)
        self.staff = StaffFactory()
        extra_field_type = ExtraFieldTypeFactory()
        extra_field_type2 = ExtraFieldTypeFactory(name='Tax Class')
        extra_field_type3 = ExtraFieldTypeFactory(name='Health',
                                                       fixed_values=False)
        extra_field_type4 = ExtraFieldTypeFactory(name='Religion',
                                                       fixed_values=False)
        extra_field = ExtraFieldFactory(field_type=extra_field_type)
        self.employee.extra_fields.add(extra_field)
        extra_field2 = ExtraFieldFactory(field_type=extra_field_type2,
                                         value='II')
        self.employee.extra_fields.add(extra_field2)
        extra_field3 = ExtraFieldFactory(field_type=extra_field_type3,
                                         value='yes')
        self.employee.extra_fields.add(extra_field3)

    def get_view_name(self):
        return 'payslip_employee_update'

    def get_view_kwargs(self):
        return {'pk': self.employee.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.manager.user)
        self.is_not_callable(user=self.employee.user)
        self.should_be_callable_when_authenticated(self.staff)
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': '{0}'.format(self.employee.user.email),
            'title': '1',
            'Tax Class': 'II',
            'Health': 'no',
            'Religion': 'None',
        }
        self.is_callable(method='POST', data=data, user=self.manager.user,
                         and_redirects_to=reverse('payslip_dashboard'))


class EmployeeDeleteViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``EmployeeDeleteView``."""
    longMessage= True

    def setUp(self):
        self.manager = ManagerFactory()
        self.employee = EmployeeFactory(company=self.manager.company)

    def get_view_name(self):
        return 'payslip_employee_delete'

    def get_view_kwargs(self):
        return {'pk': self.employee.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.manager.user)
        self.is_callable(method='POST', data={'name': 'Foo'},
                         user=self.manager.user,
                         and_redirects_to=reverse('payslip_dashboard'))


class ExtraFieldCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``ExtraFieldCreateView``."""
    longMessage= True

    def setUp(self):
        self.staff = StaffFactory()
        self.extra_field_type = ExtraFieldTypeFactory()

    def get_view_name(self):
        return 'payslip_extra_field_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        data = {
            'field_type': self.extra_field_type.id,
            'value': 'Bar',
        }
        self.is_callable(method='POST', data=data, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class ExtraFieldUpdateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``ExtraFieldUpdateView``."""
    longMessage= True

    def setUp(self):
        self.extra_field = ExtraFieldFactory()
        self.staff = StaffFactory()

    def get_view_name(self):
        return 'payslip_extra_field_update'

    def get_view_kwargs(self):
        return {'pk': self.extra_field.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)


class ExtraFieldDeleteViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``ExtraFieldDeleteView``."""
    longMessage= True

    def setUp(self):
        self.staff = StaffFactory()
        self.extra_field = ExtraFieldFactory()

    def get_view_name(self):
        return 'payslip_extra_field_delete'

    def get_view_kwargs(self):
        return {'pk': self.extra_field.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        data = {
            'field_type': self.extra_field.field_type.id,
            'value': 'Bar',
        }
        self.is_callable(method='POST', data=data, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class ExtraFieldTypeCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``ExtraFieldTypeCreateView``."""
    longMessage= True

    def setUp(self):
        self.staff = StaffFactory()

    def get_view_name(self):
        return 'payslip_extra_field_type_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'name': 'Bar'}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class ExtraFieldTypeUpdateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``ExtraFieldTypeUpdateView``."""
    longMessage= True

    def setUp(self):
        self.extra_field_type = ExtraFieldTypeFactory()
        self.staff = StaffFactory()

    def get_view_name(self):
        return 'payslip_extra_field_type_update'

    def get_view_kwargs(self):
        return {'pk': self.extra_field_type.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)


class ExtraFieldTypeDeleteViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``ExtraFieldTypeDeleteView``."""
    longMessage= True

    def setUp(self):
        self.staff = StaffFactory()
        self.extra_field_type = ExtraFieldTypeFactory()

    def get_view_name(self):
        return 'payslip_extra_field_type_delete'

    def get_view_kwargs(self):
        return {'pk': self.extra_field_type.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'name': 'Foo'}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))

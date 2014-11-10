"""Tests for the views of the ``payslip`` app."""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from django_libs.tests.factories import UserFactory
from django_libs.tests.mixins import ViewTestMixin
from payslip.tests.factories import (
    CompanyFactory,
    EmployeeFactory,
    ExtraFieldFactory,
    ExtraFieldTypeFactory,
    ManagerFactory,
    PaymentFactory,
    PaymentTypeFactory,
    StaffFactory,
)


class DashboardViewTestCase(ViewTestMixin, TestCase):
    """Tests for the TemplateView ``DashboardView``."""
    longMessage = True

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
    longMessage = True

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
    longMessage = True

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
    """Tests for the DeleteView ``CompanyDeleteView``."""
    longMessage = True

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
        self.is_callable(method='POST', data={'delete': True}, user=self.user,
                         and_redirects_to=reverse('payslip_dashboard'))


class EmployeeCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``EmployeeCreateView``."""
    longMessage = True

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
    longMessage = True

    def setUp(self):
        self.manager = ManagerFactory()
        self.employee = EmployeeFactory(company=self.manager.company)
        self.staff = StaffFactory()
        extra_field_type = ExtraFieldTypeFactory()
        extra_field_type2 = ExtraFieldTypeFactory(name='Tax Class')
        extra_field_type3 = ExtraFieldTypeFactory(name='Health',
                                                       fixed_values=False)
        ExtraFieldTypeFactory(name='Religion', fixed_values=False)
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
    """Tests for the DeleteView ``EmployeeDeleteView``."""
    longMessage = True

    def setUp(self):
        self.manager = ManagerFactory()
        self.employee = EmployeeFactory(company=self.manager.company)

    def get_view_name(self):
        return 'payslip_employee_delete'

    def get_view_kwargs(self):
        return {'pk': self.employee.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.manager.user)
        self.is_callable(method='POST', data={'delete': True},
                         user=self.manager.user,
                         and_redirects_to=reverse('payslip_dashboard'))


class ExtraFieldCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``ExtraFieldCreateView``."""
    longMessage = True

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
    longMessage = True

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
    """Tests for the DeleteView ``ExtraFieldDeleteView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.extra_field = ExtraFieldFactory()

    def get_view_name(self):
        return 'payslip_extra_field_delete'

    def get_view_kwargs(self):
        return {'pk': self.extra_field.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'delete': True}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class ExtraFieldTypeCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``ExtraFieldTypeCreateView``."""
    longMessage = True

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
    longMessage = True

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
    """Tests for the DeleteView ``ExtraFieldTypeDeleteView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.extra_field_type = ExtraFieldTypeFactory()

    def get_view_name(self):
        return 'payslip_extra_field_type_delete'

    def get_view_kwargs(self):
        return {'pk': self.extra_field_type.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'delete': True}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PaymentCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``PaymentCreateView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.payment_type = PaymentTypeFactory()
        self.employee = EmployeeFactory()

    def get_view_name(self):
        return 'payslip_payment_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        data = {
            'payment_type': self.payment_type.id,
            'employee': self.employee.id,
            'amount': '1001.00',
            'date': '2013-01-08 09:35:18',
        }
        self.is_callable(method='POST', data=data, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PaymentUpdateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``PaymentUpdateView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.payment = PaymentFactory()
        self.employee = EmployeeFactory()

    def get_view_name(self):
        return 'payslip_payment_update'

    def get_view_kwargs(self):
        return {'pk': self.payment.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        data = {
            'payment_type': self.payment.payment_type.id,
            'employee': self.employee.id,
            'amount': '1001.00',
            'date': '2013-01-08 09:35:18',
        }
        self.is_callable(method='POST', data=data, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PaymentDeleteViewTestCase(ViewTestMixin, TestCase):
    """Tests for the DeleteView ``PaymentDeleteView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.payment = PaymentFactory()

    def get_view_name(self):
        return 'payslip_payment_delete'

    def get_view_kwargs(self):
        return {'pk': self.payment.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'delete': True}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PaymentTypeCreateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the CreateView ``PaymentTypeCreateView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()

    def get_view_name(self):
        return 'payslip_payment_type_create'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'name': 'Bar'}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PaymentTypeUpdateViewTestCase(ViewTestMixin, TestCase):
    """Tests for the UpdateView ``PaymentTypeUpdateView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.payment_type = PaymentTypeFactory()

    def get_view_name(self):
        return 'payslip_payment_type_update'

    def get_view_kwargs(self):
        return {'pk': self.payment_type.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'name': 'Bar'}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PaymentTypeDeleteViewTestCase(ViewTestMixin, TestCase):
    """Tests for the DeleteView ``PaymentTypeDeleteView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.payment_type = PaymentTypeFactory()

    def get_view_name(self):
        return 'payslip_payment_type_delete'

    def get_view_kwargs(self):
        return {'pk': self.payment_type.pk}

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        self.is_callable(method='POST', data={'delete': True}, user=self.staff,
                         and_redirects_to=reverse('payslip_dashboard'))


class PayslipGeneratorViewTestCase(ViewTestMixin, TestCase):
    """Tests for the FormView ``PayslipGeneratorView``."""
    longMessage = True

    def setUp(self):
        self.staff = StaffFactory()
        self.manager = ManagerFactory()
        # Fixtures to test all context functions
        self.payment = PaymentFactory(payment_type__rrule='MONTHLY')
        self.employee = self.payment.employee
        self.employee2 = EmployeeFactory(company=self.manager.company)
        PaymentFactory(payment_type__rrule='MONTHLY', employee=self.employee,
                       date=timezone.now() - timezone.timedelta(days=365))
        PaymentFactory(payment_type__rrule='MONTHLY', employee=self.employee,
                       end_date=timezone.now() - timezone.timedelta(days=1),
                       amount=-100)

    def get_view_name(self):
        return 'payslip_generator'

    def test_view(self):
        self.should_be_callable_when_authenticated(self.staff)
        data = {
            'employee': self.employee.id,
            'year': timezone.now().year,
            'month': timezone.now().month,
        }
        self.is_callable(method='POST', data=data, user=self.staff)
        data.update({'employee': self.employee2.id})
        self.is_callable(method='POST', data=data, user=self.staff)
        data.update({'download': True})
        self.is_callable(method='POST', data=data, user=self.manager.user)

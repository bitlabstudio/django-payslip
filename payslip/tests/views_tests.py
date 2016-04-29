"""Tests for the views of the ``payslip`` app."""
from django.test import TestCase
from django.utils import timezone

from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer

from .. import views


class DashboardViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the TemplateView ``DashboardView``."""
    view_class = views.DashboardView

    def setUp(self):
        self.user = mixer.blend('auth.User')

    def test_view(self):
        self.is_not_callable(user=self.user)
        self.user.is_staff = True
        self.user.save()
        self.is_callable(user=self.user)


class CompanyCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the CreateView ``CompanyCreateView``."""
    view_class = views.CompanyCreateView

    def setUp(self):
        self.user = mixer.blend('auth.User', is_staff=True)

    def test_view(self):
        self.is_callable(user=self.user)
        self.is_postable(data={'name': 'Foo'}, user=self.user,
                         to_url_name='payslip_dashboard')


class CompanyUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the UpdateView ``CompanyUpdateView``."""
    view_class = views.CompanyUpdateView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.user.is_staff = True
        self.user.save()
        self.company = mixer.blend('payslip.Company')

    def get_view_kwargs(self):
        return {'pk': self.company.pk}

    def test_view(self):
        self.is_callable(user=self.user)


class CompanyDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the DeleteView ``CompanyDeleteView``."""
    view_class = views.CompanyDeleteView

    def setUp(self):
        self.user = mixer.blend('auth.User')
        self.company = mixer.blend('payslip.Company')

    def get_view_kwargs(self):
        return {'pk': self.company.pk}

    def test_view(self):
        self.is_not_callable(user=self.user)
        self.user.is_staff = True
        self.user.save()
        self.is_callable(user=self.user)
        self.is_postable(data={'delete': True}, user=self.user,
                         to_url_name='payslip_dashboard')


class EmployeeCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the CreateView ``EmployeeCreateView``."""
    view_class = views.EmployeeCreateView

    def setUp(self):
        self.manager = mixer.blend('payslip.Employee', is_manager=True)

    def test_view(self):
        self.is_callable(user=self.manager.user)
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'test@example.com',
            'password': 'test',
            'retype_password': 'test',
            'title': '1',
        }
        self.is_postable(data=data, user=self.manager.user,
                         to_url_name='payslip_dashboard')


class EmployeeUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the UpdateView ``EmployeeUpdateView``."""
    view_class = views.EmployeeUpdateView

    def setUp(self):
        self.manager = mixer.blend('payslip.Employee', is_manager=True)
        self.employee = mixer.blend('payslip.Employee',
                                    company=self.manager.company)
        self.staff = mixer.blend('auth.User', is_staff=True)
        extra_field_type = mixer.blend('payslip.ExtraFieldType')
        extra_field_type2 = mixer.blend('payslip.ExtraFieldType',
                                        name='Tax Class')
        extra_field_type3 = mixer.blend('payslip.ExtraFieldType',
                                        name='Health', fixed_values=False)
        mixer.blend('payslip.ExtraFieldType', name='Religion',
                    fixed_values=False)
        extra_field = mixer.blend('payslip.ExtraField',
                                  field_type=extra_field_type)
        self.employee.extra_fields.add(extra_field)
        extra_field2 = mixer.blend('payslip.ExtraField',
                                   field_type=extra_field_type2, value='II')
        self.employee.extra_fields.add(extra_field2)
        extra_field3 = mixer.blend('payslip.ExtraField',
                                   field_type=extra_field_type3, value='yes')
        self.employee.extra_fields.add(extra_field3)

    def get_view_kwargs(self):
        return {'pk': self.employee.pk}

    def test_view(self):
        self.is_callable(user=self.manager.user)
        self.is_not_callable(user=self.employee.user)
        self.is_callable(user=self.staff)
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': '{0}'.format(self.employee.user.email),
            'title': '1',
            'Tax Class': 'II',
            'Health': 'no',
            'Religion': 'None',
        }
        self.is_postable(data=data, user=self.manager.user,
                         to_url_name='payslip_dashboard')


class EmployeeDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the DeleteView ``EmployeeDeleteView``."""
    view_class = views.EmployeeDeleteView

    def setUp(self):
        self.manager = mixer.blend('payslip.Employee', is_manager=True)
        self.employee = mixer.blend('payslip.Employee',
                                    company=self.manager.company)

    def get_view_kwargs(self):
        return {'pk': self.employee.pk}

    def test_view(self):
        self.is_callable(user=self.manager.user)
        self.is_postable(data={'delete': True}, user=self.manager.user,
                         to_url_name='payslip_dashboard')


class ExtraFieldCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the CreateView ``ExtraFieldCreateView``."""
    view_class = views.ExtraFieldCreateView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.extra_field_type = mixer.blend('payslip.ExtraFieldType',
                                            fixed_values=True)

    def test_view(self):
        self.is_callable(user=self.staff)
        data = {
            'field_type': self.extra_field_type.id,
            'value': 'Bar',
        }
        self.is_postable(data=data, user=self.staff,
                         to_url_name='payslip_dashboard')


class ExtraFieldUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the UpdateView ``ExtraFieldUpdateView``."""
    view_class = views.ExtraFieldUpdateView

    def setUp(self):
        self.extra_field = mixer.blend('payslip.ExtraField')
        self.staff = mixer.blend('auth.User', is_staff=True)

    def get_view_kwargs(self):
        return {'pk': self.extra_field.pk}

    def test_view(self):
        self.is_callable(user=self.staff)


class ExtraFieldDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the DeleteView ``ExtraFieldDeleteView``."""
    view_class = views.ExtraFieldDeleteView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.extra_field = mixer.blend('payslip.ExtraField')

    def get_view_kwargs(self):
        return {'pk': self.extra_field.pk}

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'delete': True}, user=self.staff,
                         to_url_name='payslip_dashboard')


class ExtraFieldTypeCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the CreateView ``ExtraFieldTypeCreateView``."""
    view_class = views.ExtraFieldTypeCreateView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'name': 'Bar'}, user=self.staff,
                         to_url_name='payslip_dashboard')


class ExtraFieldTypeUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the UpdateView ``ExtraFieldTypeUpdateView``."""
    view_class = views.ExtraFieldTypeUpdateView

    def setUp(self):
        self.extra_field_type = mixer.blend('payslip.ExtraFieldType')
        self.staff = mixer.blend('auth.User', is_staff=True)

    def get_view_kwargs(self):
        return {'pk': self.extra_field_type.pk}

    def test_view(self):
        self.is_callable(user=self.staff)


class ExtraFieldTypeDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the DeleteView ``ExtraFieldTypeDeleteView``."""
    view_class = views.ExtraFieldTypeDeleteView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.extra_field_type = mixer.blend('payslip.ExtraFieldType')

    def get_view_kwargs(self):
        return {'pk': self.extra_field_type.pk}

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'delete': True}, user=self.staff,
                         to_url_name='payslip_dashboard')


class PaymentCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the CreateView ``PaymentCreateView``."""
    view_class = views.PaymentCreateView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.payment_type = mixer.blend('payslip.PaymentType')
        self.employee = mixer.blend('payslip.Employee')

    def test_view(self):
        self.is_callable(user=self.staff)
        data = {
            'payment_type': self.payment_type.id,
            'employee': self.employee.id,
            'amount': '1001.00',
            'date': '2013-01-08 09:35:18',
        }
        self.is_postable(data=data, user=self.staff,
                         to_url_name='payslip_dashboard')


class PaymentUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the UpdateView ``PaymentUpdateView``."""
    view_class = views.PaymentUpdateView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.payment = mixer.blend('payslip.Payment')
        self.employee = mixer.blend('payslip.Employee')

    def get_view_kwargs(self):
        return {'pk': self.payment.pk}

    def test_view(self):
        self.is_callable(user=self.staff)
        data = {
            'payment_type': self.payment.payment_type.id,
            'employee': self.employee.id,
            'amount': '1001.00',
            'date': '2013-01-08 09:35:18',
        }
        self.is_postable(data=data, user=self.staff,
                         to_url_name='payslip_dashboard')


class PaymentDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the DeleteView ``PaymentDeleteView``."""
    view_class = views.PaymentDeleteView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.payment = mixer.blend('payslip.Payment')

    def get_view_kwargs(self):
        return {'pk': self.payment.pk}

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'delete': True}, user=self.staff,
                         to_url_name='payslip_dashboard')


class PaymentTypeCreateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the CreateView ``PaymentTypeCreateView``."""
    view_class = views.PaymentTypeCreateView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'name': 'Bar'}, user=self.staff,
                         to_url_name='payslip_dashboard')


class PaymentTypeUpdateViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the UpdateView ``PaymentTypeUpdateView``."""
    view_class = views.PaymentTypeUpdateView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.payment_type = mixer.blend('payslip.PaymentType')

    def get_view_kwargs(self):
        return {'pk': self.payment_type.pk}

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'name': 'Bar'}, user=self.staff,
                         to_url_name='payslip_dashboard')


class PaymentTypeDeleteViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the DeleteView ``PaymentTypeDeleteView``."""
    view_class = views.PaymentTypeDeleteView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.payment_type = mixer.blend('payslip.PaymentType')

    def get_view_kwargs(self):
        return {'pk': self.payment_type.pk}

    def test_view(self):
        self.is_callable(user=self.staff)
        self.is_postable(data={'delete': True}, user=self.staff,
                         to_url_name='payslip_dashboard')


class PayslipGeneratorViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    """Tests for the FormView ``PayslipGeneratorView``."""
    view_class = views.PayslipGeneratorView

    def setUp(self):
        self.staff = mixer.blend('auth.User', is_staff=True)
        self.manager = mixer.blend('payslip.Employee', is_manager=True)
        # Fixtures to test all context functions
        self.payment = mixer.blend('payslip.Payment',
                                   payment_type__rrule='MONTHLY')
        self.employee = self.payment.employee
        self.employee2 = mixer.blend('payslip.Employee',
                                     company=self.manager.company)
        mixer.blend('payslip.Payment', payment_type__rrule='MONTHLY',
                    employee=self.employee,
                    date=timezone.now() - timezone.timedelta(days=365))
        mixer.blend('payslip.Payment', payment_type__rrule='MONTHLY',
                    employee=self.employee, amount=-100,
                    end_date=timezone.now() - timezone.timedelta(days=1))

    def test_view(self):
        self.is_callable(user=self.staff)
        data = {
            'employee': self.employee.id,
            'year': timezone.now().year,
            'month': timezone.now().month,
        }
        self.is_postable(data=data, user=self.staff, ajax=True)
        data.update({'employee': self.employee2.id})
        self.is_postable(data=data, user=self.staff, ajax=True)
        data.update({'download': True})
        self.is_postable(data=data, user=self.manager.user, ajax=True)

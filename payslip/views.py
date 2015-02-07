"""Views for the ``online_docs`` app."""
import cStringIO as StringIO
from datetime import datetime
import os

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
)

from dateutil import relativedelta, rrule
from xhtml2pdf import pisa

from .app_settings import CURRENCY
from .forms import (
    EmployeeForm,
    ExtraFieldForm,
    PaymentForm,
    PayslipForm,
)
from .models import (
    Company,
    Employee,
    ExtraField,
    ExtraFieldType,
    Payment,
    PaymentType,
)


# -------------#
# Mixins       #
# -------------#

class PermissionMixin(object):
    """Mixin to handle security functions."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Makes sure that the user is logged in and has the right to display this
        view.

        """
        if not request.user.is_staff:
            raise Http404
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('payslip_dashboard')


class CompanyMixin(object):
    """Mixin to handle company related functions."""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Makes sure that the user is logged in and has the right to display this
        view.

        """
        self.kwargs = kwargs
        self.object = self.get_object()
        try:
            Employee.objects.get(company=self.object, user=request.user,
                                 is_manager=True)
        except Employee.DoesNotExist:
            if not request.user.is_staff:
                raise Http404
        return super(CompanyMixin, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('payslip_dashboard')


class CompanyPermissionMixin(object):
    """Mixin to handle company-wide permissions functions."""

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Makes sure that the user is logged in and has the right to display this
        view.

        """
        try:
            self.company = Employee.objects.get(
                user=request.user, is_manager=True).company
        except Employee.DoesNotExist:
            if not request.user.is_staff:
                raise Http404
            self.company = None
        return super(CompanyPermissionMixin, self).dispatch(request, *args,
                                                            **kwargs)

    def get_success_url(self):
        return reverse('payslip_dashboard')


class EmployeeMixin(object):
    """Mixin to handle employee related functions."""
    form_class = EmployeeForm

    def get_form_kwargs(self):
        kwargs = super(EmployeeMixin, self).get_form_kwargs()
        kwargs.update({'company': self.company})
        return kwargs


class ExtraFieldMixin(object):
    """Mixin to handle extra field related functions."""
    model = ExtraField
    form_class = ExtraFieldForm


class ExtraFieldTypeMixin(object):
    """Mixin to handle extra field type related functions."""
    model = ExtraFieldType


class PaymentMixin(object):
    """Mixin to handle payment related functions."""
    model = Payment
    form_class = PaymentForm


class PaymentTypeMixin(object):
    """Mixin to handle payment type related functions."""
    model = PaymentType


# -------------#
# Views        #
# -------------#

class DashboardView(PermissionMixin, TemplateView):
    """Dashboard to navigate through the payslip app."""
    template_name = 'payslip/dashboard.html'

    def get_context_data(self, **kwargs):
        return {
            'companies': Company.objects.all(),
            'employees': Employee.objects.all(),
            'extra_field_types': ExtraFieldType.objects.all(),
            'fixed_value_extra_fields': ExtraField.objects.filter(
                field_type__fixed_values=True),
            'payments': Payment.objects.all(),
            'payment_types': PaymentType.objects.all(),
        }


class CompanyCreateView(PermissionMixin, CreateView):
    """Classic view to create a company."""
    model = Company

    def get_success_url(self):
        return reverse('payslip_dashboard')


class CompanyUpdateView(CompanyMixin, UpdateView):
    """Classic view to update a company."""
    model = Company


class CompanyDeleteView(CompanyMixin, DeleteView):
    """Classic view to delete a company."""
    model = Company


class EmployeeCreateView(CompanyPermissionMixin, EmployeeMixin, CreateView):
    """Classic view to create an employee."""
    model = Employee


class EmployeeUpdateView(CompanyPermissionMixin, EmployeeMixin, UpdateView):
    """Classic view to update an employee."""
    model = Employee


class EmployeeDeleteView(CompanyPermissionMixin, EmployeeMixin, DeleteView):
    """Classic view to delete an employee."""
    model = Employee


class ExtraFieldTypeCreateView(PermissionMixin, ExtraFieldTypeMixin,
                               CreateView):
    """Classic view to create an extra field type."""
    pass


class ExtraFieldTypeUpdateView(PermissionMixin, ExtraFieldTypeMixin,
                               UpdateView):
    """Classic view to update an extra field type."""
    pass


class ExtraFieldTypeDeleteView(PermissionMixin, ExtraFieldTypeMixin,
                               DeleteView):
    """Classic view to delete an extra field type."""
    pass


class ExtraFieldCreateView(PermissionMixin, ExtraFieldMixin, CreateView):
    """Classic view to create an extra field."""
    pass


class ExtraFieldUpdateView(PermissionMixin, ExtraFieldMixin, UpdateView):
    """Classic view to update an extra field."""
    pass


class ExtraFieldDeleteView(PermissionMixin, ExtraFieldMixin, DeleteView):
    """Classic view to delete an extra field."""
    pass


class PaymentTypeCreateView(CompanyPermissionMixin, PaymentTypeMixin,
                            CreateView):
    """Classic view to create a payment type."""
    pass


class PaymentTypeUpdateView(CompanyPermissionMixin, PaymentTypeMixin,
                            UpdateView):
    """Classic view to update a payment type."""
    pass


class PaymentTypeDeleteView(CompanyPermissionMixin, PaymentTypeMixin,
                            DeleteView):
    """Classic view to delete a payment type."""
    pass


class PaymentCreateView(CompanyPermissionMixin, PaymentMixin, CreateView):
    """Classic view to create a payment."""
    pass


class PaymentUpdateView(CompanyPermissionMixin, PaymentMixin, UpdateView):
    """Classic view to update a payment."""
    pass


class PaymentDeleteView(CompanyPermissionMixin, PaymentMixin, DeleteView):
    """Classic view to delete a payment."""
    pass


class PayslipGeneratorView(CompanyPermissionMixin, FormView):
    """View to present a small form to generate a custom payslip."""
    template_name = 'payslip/payslip_form.html'
    form_class = PayslipForm

    def get_form_kwargs(self):
        kwargs = super(PayslipGeneratorView, self).get_form_kwargs()
        kwargs.update({'company': self.company})
        return kwargs

    def get_template_names(self):
        if hasattr(self, 'post_data'):
            return ['payslip/payslip.html']
        return super(PayslipGeneratorView, self).get_template_names()

    def get_context_data(self, **kwargs):
        kwargs = super(PayslipGeneratorView, self).get_context_data(**kwargs)
        if hasattr(self, 'post_data'):
            # Get form data
            employee = Employee.objects.get(pk=self.post_data.get('employee'))
            date_start = datetime.strptime(
                '{}-{}-01'.format(
                    self.post_data.get('year'), self.post_data.get('month')),
                '%Y-%m-%d',
            )
            january_1st = datetime.strptime(
                '{}-01-01'.format(self.post_data.get('year')),
                '%Y-%m-%d',
            )
            date_end = (date_start + relativedelta.relativedelta(months=1)
                        - relativedelta.relativedelta(days=1))

            # Get payments for the selected year
            payments_year = employee.payments.filter(
                # Recurring payments with past date and end_date in the
                # selected year or later
                Q(date__lte=date_end, end_date__gte=january_1st) |
                # Recurring payments with past date in period and open end
                Q(date__lte=date_end, end_date__isnull=True,
                  payment_type__rrule__isnull=False)
            ).exclude(payment_type__rrule__exact='') | employee.payments.filter(
                # Single payments in this year
                date__year=date_start.year, payment_type__rrule__exact='',
            )

            # Get payments for the selected period
            payments = payments_year.exclude(
                # Exclude single payments not transferred in the period
                Q(date__lt=date_start) |
                Q(date__gt=date_end),
                Q(payment_type__rrule__exact=''),
            ).filter(
                # Recurring payments with past date and end_date in the period
                Q(end_date__gte=date_end, date__lte=date_end) |
                # Recurring payments with past date in period and open end
                Q(date__lte=date_end, end_date__isnull=True)
            )

            # Yearly positive summary
            sum_year = payments_year.filter(
                amount__gt=0, payment_type__rrule__exact='').aggregate(
                    Sum('amount')).get('amount__sum') or 0

            # Yearly negative summary
            sum_year_neg = payments_year.filter(
                amount__lt=0, payment_type__rrule__exact='').aggregate(
                    Sum('amount')).get('amount__sum') or 0

            # Yearly summary of recurring payments
            for payment in payments_year.exclude(
                    payment_type__rrule__exact=''):
                # If the recurring payment started in a year before, let's take
                # January 1st as a start, otherwise take the original date
                if payment.get_date_without_tz().year < date_start.year:
                    start = january_1st
                else:
                    start = payment.get_date_without_tz()
                # If the payments ends before the period's end date, let's take
                # this date, otherwise we can take the period's end
                if (payment.end_date
                        and payment.get_end_date_without_tz() < date_end):
                    end = payment.get_end_date_without_tz()
                else:
                    end = date_end
                recurrings = rrule.rrule(
                    rrule._rrulestr._freq_map.get(payment.payment_type.rrule),
                    dtstart=start, until=end,
                )
                # Multiply amount with recurrings
                if payment.amount > 0:
                    sum_year += payment.amount * recurrings.count()
                else:
                    sum_year_neg += payment.amount * recurrings.count()

            # Period summaries
            sum = payments.filter(amount__gt=0).aggregate(
                Sum('amount')).get('amount__sum') or 0
            sum_neg = payments.filter(amount__lt=0).aggregate(
                Sum('amount')).get('amount__sum') or 0

            kwargs.update({
                'employee': employee,
                'date_start': date_start,
                'date_end': date_end,
                'payments': payments,
                'payment_extra_fields': ExtraFieldType.objects.filter(
                    model='Payment'),
                'sum_year': sum_year,
                'sum_year_neg': sum_year + sum_year_neg,
                'sum': sum,
                'sum_neg': sum_neg,
                'currency': CURRENCY,
            })
        return kwargs

    def form_valid(self, form):
        self.post_data = self.request.POST
        if 'download' in self.post_data:
            result = StringIO.StringIO()
            html = self.render_to_response(self.get_context_data(form=form))
            f = open(os.path.join(
                os.path.dirname(__file__), './static/payslip/css/payslip.css'))
            pdf = pisa.CreatePDF(html.render().content, result,
                                 default_css=f.read())
            f.close()
            if not pdf.err:
                return HttpResponse(result.getvalue(),
                                    mimetype='application/pdf')
        return self.render_to_response(self.get_context_data(form=form))

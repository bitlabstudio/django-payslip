"""Views for the ``online_docs`` app."""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView,
)

from payslip.forms import EmployeeForm, ExtraFieldForm
from payslip.models import Company, Employee, ExtraField, ExtraFieldType


#-------------#
# Mixins      #
#-------------#

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


class EmployeeMixin(object):
    """Mixin to handle employee related functions."""
    form_class = EmployeeForm

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
        return super(EmployeeMixin, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EmployeeMixin, self).get_form_kwargs()
        kwargs.update({'company': self.company})
        return kwargs

    def get_success_url(self):
        return reverse('payslip_dashboard')


class ExtraFieldMixin(object):
    """Mixin to handle extra field related functions."""
    model = ExtraField
    form_class = ExtraFieldForm

    def get_success_url(self):
        return reverse('payslip_dashboard')


class ExtraFieldTypeMixin(object):
    """Mixin to handle extra field type related functions."""
    model = ExtraFieldType

    def get_success_url(self):
        return reverse('payslip_dashboard')


#-------------#
# Views       #
#-------------#

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


class EmployeeCreateView(EmployeeMixin, CreateView):
    """Classic view to create an employee."""
    model = Employee


class EmployeeUpdateView(EmployeeMixin, UpdateView):
    """Classic view to update an employee."""
    model = Employee


class EmployeeDeleteView(EmployeeMixin, DeleteView):
    """Classic view to delete an employee."""
    model = Employee


class ExtraFieldTypeCreateView(PermissionMixin, ExtraFieldTypeMixin,
                               CreateView):
    """Classic view to create an extra field type."""
    model = ExtraFieldType


class ExtraFieldTypeUpdateView(PermissionMixin, ExtraFieldTypeMixin,
                               UpdateView):
    """Classic view to update an extra field type."""
    model = ExtraFieldType


class ExtraFieldTypeDeleteView(PermissionMixin, ExtraFieldTypeMixin,
                               DeleteView):
    """Classic view to delete an extra field type."""
    model = ExtraFieldType


class ExtraFieldCreateView(PermissionMixin, ExtraFieldMixin, CreateView):
    """Classic view to create an extra field."""
    model = ExtraField


class ExtraFieldUpdateView(PermissionMixin, ExtraFieldMixin, UpdateView):
    """Classic view to update an extra field."""
    model = ExtraField


class ExtraFieldDeleteView(PermissionMixin, ExtraFieldMixin, DeleteView):
    """Classic view to delete an extra field."""
    model = ExtraField

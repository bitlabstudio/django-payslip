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

from payslip.models import Company, Employee


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
    model = Company

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Makes sure that the user is logged in and has the right to display this
        view.

        """
        self.kwargs = kwargs
        self.object = self.get_object()
        try:
            Employee.objects.get(company=self.object, user=request.user)
        except Employee.DoesNotExist:
            if not request.user.is_staff:
                raise Http404
        return super(CompanyMixin, self).dispatch(request, *args, **kwargs)

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
        }


class CompanyCreateView(PermissionMixin, CreateView):
    """Classic view to create a company."""
    model = Company

    def get_success_url(self):
        return reverse('payslip_company_update', kwargs={'pk': self.object.id})


class CompanyUpdateView(CompanyMixin, UpdateView):
    """Classic view to update a company."""
    pass


class CompanyDeleteView(CompanyMixin, DeleteView):
    """Classic view to delete a company."""
    pass

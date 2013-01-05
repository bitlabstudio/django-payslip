"""Views for the ``online_docs`` app."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """DUmmy view. Should be deleted and replaced with real views."""
    template_name = 'payslip/home.html'

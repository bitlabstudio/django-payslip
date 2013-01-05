"""URLs for the ``online_docs`` app."""
from django.conf.urls.defaults import patterns, url, include

from payslip.views import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyUpdateView,
    DashboardView,
)


urlpatterns = patterns(
    '',
    (r'^accounts/', include('registration.backends.default.urls')),

    url(r'^$',
        DashboardView.as_view(),
        name='payslip_dashboard',
    ),

    url(r'^company/create/$',
        CompanyCreateView.as_view(),
        name='payslip_company_create',
    ),

    url(r'^company/(?P<pk>\d+)/update/$',
        CompanyUpdateView.as_view(),
        name='payslip_company_update',
    ),

    url(r'^company/(?P<pk>\d+)/delete/$',
        CompanyDeleteView.as_view(),
        name='payslip_company_delete',
    ),
)

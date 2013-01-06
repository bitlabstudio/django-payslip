"""URLs for the ``online_docs`` app."""
from django.conf.urls.defaults import patterns, url, include

from payslip.views import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyUpdateView,
    EmployeeCreateView,
    EmployeeDeleteView,
    EmployeeUpdateView,
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

    url(r'^employee/create/$',
        EmployeeCreateView.as_view(),
        name='payslip_employee_create',
    ),

    url(r'^employee/(?P<pk>\d+)/update/$',
        EmployeeUpdateView.as_view(),
        name='payslip_employee_update',
    ),

    url(r'^employee/(?P<pk>\d+)/delete/$',
        EmployeeDeleteView.as_view(),
        name='payslip_employee_delete',
    ),
)

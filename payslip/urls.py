"""URLs for the ``online_docs`` app."""
from django.conf.urls import patterns, url

from payslip.views import (
    CompanyCreateView,
    CompanyDeleteView,
    CompanyUpdateView,
    EmployeeCreateView,
    EmployeeDeleteView,
    EmployeeUpdateView,
    ExtraFieldCreateView,
    ExtraFieldDeleteView,
    ExtraFieldUpdateView,
    ExtraFieldTypeCreateView,
    ExtraFieldTypeDeleteView,
    ExtraFieldTypeUpdateView,
    DashboardView,
    PaymentCreateView,
    PaymentDeleteView,
    PaymentUpdateView,
    PaymentTypeCreateView,
    PaymentTypeDeleteView,
    PaymentTypeUpdateView,
    PayslipGeneratorView,
)


urlpatterns = patterns(
    '',
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

    url(r'^extra-field/create/$',
        ExtraFieldCreateView.as_view(),
        name='payslip_extra_field_create',
        ),

    url(r'^extra-field/(?P<pk>\d+)/update/$',
        ExtraFieldUpdateView.as_view(),
        name='payslip_extra_field_update',
        ),

    url(r'^extra-field/(?P<pk>\d+)/delete/$',
        ExtraFieldDeleteView.as_view(),
        name='payslip_extra_field_delete',
        ),

    url(r'^extra-field-type/create/$',
        ExtraFieldTypeCreateView.as_view(),
        name='payslip_extra_field_type_create',
        ),

    url(r'^extra-field-type/(?P<pk>\d+)/update/$',
        ExtraFieldTypeUpdateView.as_view(),
        name='payslip_extra_field_type_update',
        ),

    url(r'^extra-field-type/(?P<pk>\d+)/delete/$',
        ExtraFieldTypeDeleteView.as_view(),
        name='payslip_extra_field_type_delete',
        ),

    url(r'^payment/create/$',
        PaymentCreateView.as_view(),
        name='payslip_payment_create',
        ),

    url(r'^payment/(?P<pk>\d+)/update/$',
        PaymentUpdateView.as_view(),
        name='payslip_payment_update',
        ),

    url(r'^payment/(?P<pk>\d+)/delete/$',
        PaymentDeleteView.as_view(),
        name='payslip_payment_delete',
        ),

    url(r'^payment-type/create/$',
        PaymentTypeCreateView.as_view(),
        name='payslip_payment_type_create',
        ),

    url(r'^payment-type/(?P<pk>\d+)/update/$',
        PaymentTypeUpdateView.as_view(),
        name='payslip_payment_type_update',
        ),

    url(r'^payment-type/(?P<pk>\d+)/delete/$',
        PaymentTypeDeleteView.as_view(),
        name='payslip_payment_type_delete',
        ),

    url(r'^payslip/$',
        PayslipGeneratorView.as_view(),
        name='payslip_generator',
        ),
)

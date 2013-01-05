"""URLs for the ``online_docs`` app."""
from django.conf.urls.defaults import patterns, url

from payslip.views import HomeView


urlpatterns = patterns(
    '',
    url(r'^$',
        HomeView.as_view(),
        name='payslip_home',
    )
)

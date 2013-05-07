"""Settings of the ``payslip``` application."""
from django.conf import settings

CURRENCY = getattr(settings, 'PAYSLIP_CURRENCY', 'EUR')

"""Variable filters for the ``payslip```application."""
from django.template.base import Library
from django.utils.safestring import mark_safe

from payslip.models import ExtraField

register = Library()


@register.filter(is_safe=True)
def get_extra_field_value(field_type, payment):
    """Returns the value of a specific field type."""
    try:
        return payment.extra_fields.get(field_type=field_type).value
    except ExtraField.DoesNotExist:
        return mark_safe('&nbsp;')

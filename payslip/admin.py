"""Admin classes for the payslip app."""
from django.contrib import admin

from . import models


admin.site.register(models.Company)
admin.site.register(models.Employee)
admin.site.register(models.ExtraField)
admin.site.register(models.ExtraFieldType)
admin.site.register(models.Payment)
admin.site.register(models.PaymentType)

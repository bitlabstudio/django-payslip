"""
Utilities and helper functions for all tests of ``django-payslip``.

The tools in this module shall help to create test fixtures for models that are
global to the project and could be shared by tests of specialized apps.

"""
import factory
from payslip.models import Company


class CompanyFactory(factory.Factory):
    """Factory for the model ``Company``."""
    FACTORY_FOR = Company

    name = 'Test Company'

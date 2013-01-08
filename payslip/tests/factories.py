"""
Utilities and helper functions for all tests of ``django-payslip``.

The tools in this module shall help to create test fixtures for models that are
global to the project and could be shared by tests of specialized apps.

"""
from django_libs.tests.factories import UserFactory
import factory
from payslip.models import Company, Employee, ExtraField, ExtraFieldType


class StaffFactory(UserFactory):
    """Enhanced factory for the model ``User``."""
    is_staff = True


class CompanyFactory(factory.Factory):
    """Factory for the model ``Company``."""
    FACTORY_FOR = Company

    name = 'Test Company'


class EmployeeFactory(factory.Factory):
    """Factory for the model ``Employee``."""
    FACTORY_FOR = Employee

    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(CompanyFactory)
    title = 0


class ManagerFactory(factory.Factory):
    """Factory for the model ``Employee`` with extra permission."""
    FACTORY_FOR = Employee

    user = factory.SubFactory(StaffFactory)
    company = factory.SubFactory(CompanyFactory)
    title = 0
    is_manager = True


class ExtraFieldTypeFactory(factory.Factory):
    """Factory for the model ``ExtraFieldType``."""
    FACTORY_FOR = ExtraFieldType

    name = 'Foo'
    fixed_values = True
    model = 'Employee'


class ExtraFieldFactory(factory.Factory):
    """Factory for the model ``ExtraField``."""
    FACTORY_FOR = ExtraField

    field_type = factory.SubFactory(ExtraFieldTypeFactory)
    value = 'Foo'

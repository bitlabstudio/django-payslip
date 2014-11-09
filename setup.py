import os
from setuptools import setup, find_packages
import payslip


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-payslip",
    version=payslip.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, payslip',
    author='Tobias Lorenz',
    author_email='tobias.lorenz@bitmazk@.com',
    url="https://github.com/bitmazk/django-payslip",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
        'xhtml2pdf',
    ],
    tests_require=[
        'fabric',
        'factory_boy',
        'django-nose',
        'coverage',
        'django-coverage',
        'mock',
        'selenium',
    ],
    test_suite='payslip.tests.runtests.runtests',
)

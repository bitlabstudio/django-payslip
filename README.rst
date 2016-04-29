Django Payslip
==============

A reusable Django app that allows you to enter salary data of your employees
so that authorized persons can view, print and export (PDF) their payslips.

Installation
------------

You need to install the following prerequisites in order to use this app::

    pip install Django
    pip install django-libs
    pip install python-dateutil
    pip install WeasyPrint

If you want to install the latest stable release from PyPi::

    $ pip install django-payslip

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-payslip.git#egg=payslip

Add ``payslip`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'payslip',
    )

Hook this app into your ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^payslip/', include('payslip.urls')),
    )


Features & Usage
----------------

You can:

    * Define companies
    * Assign employees (a user model is created automatically)
    * Define payment types
    * Create payments
    * Create custom extra fields for COMPANIES, EMPLOYEES and PAYMENTS
    * Create global attributes for those custom fields (dropdown fields)
    * Generate custom payslips
    * Print those payslips or export them as styled PDF documents

There's already a print-ready template for your payslips, which should cover
mainly used payslips. If you want to you can override the template with your
own styles. Find it here ``payslip/templates/payslip/payslip.html``.

You can also create your own CSS, but be sure to cover print styles. Find it
here ``static/payslip/css/payslip.css``.

After you have added the basic company information needed in your template, you
can add payments and employees and start paysliping. :) Have fun with it.


Settings
--------

PAYSLIP_CURRENCY
++++++++++++++++

Default: 'EUR'

Your preferred currency acronym.


Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 payslip
    $ pip install -r requirements.txt
    $ ./payslip/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.

If you are making changes that need to be tested in a browser (i.e. to the
CSS or JS files), you might want to setup a Django project, follow the
installation instructions above, then run ``python setup.py develop``. This
will just place an egg-link to your cloned fork in your project's virtualenv.

Roadmap
-------

* Add employee and manager dashboards

Check the issue tracker on github for further milestones and features to come.

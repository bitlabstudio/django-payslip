""" Forms for the `payslip` app. """
import md5

from django.contrib.auth.models import make_password, User
from django import forms
from django.utils.translation import ugettext_lazy as _

from payslip.models import Company, Employee


def get_md5_hexdigest(email):
    """
    Returns an md5 hash for a given email.

    The length is 30 so that it fits into Django's ``User.username`` field.

    """
    return md5.new(email).hexdigest()[0:30]


def generate_username(email):
    """
    Generates a unique username for the given email.

    The username will be an md5 hash of the given email. If the username exists
    we just append `a` to the email until we get a unique md5 hash.

    """
    username = get_md5_hexdigest(email)
    found_unique_username = False
    while not found_unique_username:
        try:
            User.objects.get(username=username)
            email = '{0}a'.format(email)
            username = get_md5_hexdigest(email)
        except User.DoesNotExist:
            found_unique_username = True
            return username


class EmployeeForm(forms.ModelForm):
    """
    Form to create a new Employee instance.

    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), max_length=128)
    retype_password = forms.CharField(widget=forms.PasswordInput(),
                                      max_length=128)

    def __init__(self, company, *args, **kwargs):
        self.company = company
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if self.company and self.company.pk:
            del self.fields['company']

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            _('A user with that email already exists.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields match.

        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.

        """
        data = self.cleaned_data
        if not 'email' in data:
            return data
        if ('password' in data and 'retype_password' in data):
            if data['password'] != data['retype_password']:
                raise forms.ValidationError(
                    _("The two password fields didn't match."))

        self.cleaned_data['username'] = generate_username(data['email'])
        return self.cleaned_data

    def save(self, *args, **kwargs):
        user = User(
            username=self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=make_password(self.cleaned_data.get('password')),
        )
        user.save()
        self.instance.user = user
        if self.company and self.company.pk:
            self.instance.company = Company.objects.get(pk=self.company.pk)
        return super(EmployeeForm, self).save(*args, **kwargs)

    class Meta:
        model = Employee
        exclude = ('user')

"""Forms for the ``payslip`` app."""
import md5

from django.contrib.auth.models import make_password, User
from django.db.models import Q
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from dateutil.relativedelta import relativedelta

from payslip.models import (
    Company,
    Employee,
    ExtraField,
    ExtraFieldType,
    Payment,
)


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


class ExtraFieldFormMixin(object):
    """Mixin to handle extra field related functions."""
    def __init__(self, *args, **kwargs):
        self.extra_field_types = ExtraFieldType.objects.filter(
            Q(model=self.Meta.model.__name__) | Q(model__isnull=True))
        if kwargs.get('instance'):
            for extra_field_type in self.extra_field_types:
                try:
                    field = kwargs.get('instance').extra_fields.get(
                        field_type__name=extra_field_type.name)
                except ExtraField.DoesNotExist:
                    pass
                else:
                    kwargs['initial'].update({'{0}'.format(
                        extra_field_type.name): field.value})
        super(ExtraFieldFormMixin, self).__init__(*args, **kwargs)
        for extra_field_type in self.extra_field_types:
            if extra_field_type.fixed_values:
                choices = [(x.value, x.value)
                           for x in extra_field_type.extra_fields.all()]
                choices.append(('', '-----'))
                self.fields[extra_field_type.name] = forms.ChoiceField(
                    required=False,
                    choices=list(set(choices)),
                )
            else:
                self.fields[extra_field_type.name] = forms.CharField(
                    required=False, max_length=200)

    def save(self, *args, **kwargs):
        resp = super(ExtraFieldFormMixin, self).save(*args, **kwargs)
        for extra_field_type in self.extra_field_types:
            try:
                field_to_save = self.instance.extra_fields.get(
                    field_type__name=extra_field_type.name)
            except ExtraField.DoesNotExist:
                field_to_save = None
            if extra_field_type.fixed_values:
                if field_to_save:
                    self.instance.extra_fields.remove(
                        self.instance.extra_fields.get(
                            field_type__name=extra_field_type.name))
                try:
                    field_to_save = ExtraField.objects.get(
                        field_type__name=extra_field_type.name,
                        value=self.data.get(extra_field_type.name))
                except ExtraField.DoesNotExist:
                    pass
                else:
                    self.instance.extra_fields.add(field_to_save)
            else:
                if field_to_save:
                    field_to_save.value = self.data.get(extra_field_type.name)
                    field_to_save.save()
                elif self.data.get(extra_field_type.name):
                    new_field = ExtraField(
                        field_type=extra_field_type,
                        value=self.data.get(extra_field_type.name),
                    )
                    new_field.save()
                    self.instance.extra_fields.add(new_field)
        return resp


class EmployeeForm(ExtraFieldFormMixin, forms.ModelForm):
    """Form to create a new Employee instance."""
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), max_length=128)
    retype_password = forms.CharField(widget=forms.PasswordInput(),
                                      max_length=128)

    def __init__(self, company, *args, **kwargs):
        self.company = company
        if kwargs.get('instance'):
            instance = kwargs.get('instance')
            user = instance.user
            kwargs['initial'] = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        super(EmployeeForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            del self.fields['password']
            del self.fields['retype_password']
        if self.company and self.company.pk:
            del self.fields['company']

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        if self.instance.id and user == self.instance.user:
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
        if 'email' not in data:
            return data
        if ('password' in data and 'retype_password' in data):
            if data['password'] != data['retype_password']:
                raise forms.ValidationError(
                    _("The two password fields didn't match."))

        self.cleaned_data['username'] = generate_username(data['email'])
        return self.cleaned_data

    def save(self, *args, **kwargs):
        if self.instance.id:
            User.objects.filter(pk=self.instance.user.pk).update(
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
            )
        else:
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
        fields = ('company', 'hr_number', 'address', 'title', 'is_manager')


class PaymentForm(ExtraFieldFormMixin, forms.ModelForm):
    """Form to create a new Payment instance."""
    class Meta:
        model = Payment
        fields = ('payment_type', 'employee', 'amount', 'date', 'end_date',
                  'description')


class ExtraFieldForm(forms.ModelForm):
    """Form to create a new ExtraField instance."""
    def __init__(self, *args, **kwargs):
        super(ExtraFieldForm, self).__init__(*args, **kwargs)
        self.fields['field_type'].queryset = ExtraFieldType.objects.filter(
            fixed_values=True)

    class Meta:
        model = ExtraField


class PayslipForm(forms.Form):
    """Form to create a custom payslip."""
    year = forms.ChoiceField()
    month = forms.ChoiceField()
    employee = forms.ChoiceField()

    def __init__(self, company, *args, **kwargs):
        super(PayslipForm, self).__init__(*args, **kwargs)
        last_month = timezone.now().replace(day=1) - relativedelta(months=1)
        self.fields['month'].choices = (
            (1, _('January')),
            (2, _('February')),
            (3, _('March')),
            (4, _('April')),
            (5, _('May')),
            (6, _('June')),
            (7, _('July')),
            (8, _('August')),
            (9, _('September')),
            (10, _('October')),
            (11, _('November')),
            (12, _('December')),
        )
        self.fields['month'].initial = last_month.month
        current_year = timezone.now().year
        self.fields['year'].choices = [
            (current_year - x, current_year - x) for x in range(0, 20)]
        self.fields['year'].initial = last_month.year
        self.company = company
        if self.company:
            self.fields['employee'].choices = [(
                x.id, x) for x in self.company.employees.all()]
        else:
            self.fields['employee'].choices = [(
                x.id, x) for x in Employee.objects.all()]

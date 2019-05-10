from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import ProfileOrganization, ProfilePerson
from django.db import transaction


class FormRegisterPerson(UserCreationForm):
    is_person = forms.BooleanField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_person = True
        user.save()
        return user


class FormRegisterOrg(UserCreationForm):
    # name = forms.CharField(max_length=255)
    # type = forms.ChoiceField()
    # country = forms.ChoiceField()
    is_org = forms.BooleanField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_org = True
        user.save()
        return user


class FormUserUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name','last_name']


class FormProfilePersonUpdate(forms.ModelForm):
    class Meta:
        model = ProfilePerson
        fields= ['gender','birth_date','nationality','bio', 'phone']


class FormProfileOrgUpdate(forms.ModelForm):
    class Meta:
        model = ProfileOrganization
        fields=['name','type','description','phone']

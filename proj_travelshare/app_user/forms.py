from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import ProfileOrganization,ProfilePerson

class FormRegister(UserCreationForm):
    email = forms.EmailField()
    person = forms.BooleanField()
    org = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FormUserUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['first_name','last_name']


class FormProfilePersonUpdate(forms.ModelForm):
    class Meta:
        model = ProfilePerson
        fields= []


class FormProfileOrgUpdate(forms.ModelForm):
    class Meta:
        model = ProfilePerson
        fields=[]

from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import ProfileTraveler, ProfileHost
from django.db import transaction


class FormRegister(UserCreationForm):
    class Meta():
        model = User
        fields = ['type', 'username', 'email', 'password1', 'password2']
        widgets = {'type': forms.RadioSelect,}

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     if self.type == '0' or self.type == '1':
    #         user.save()
    #     return user


class FormUserUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class FormProfileTravelerUpdate(forms.ModelForm):
    class Meta:
        model = ProfileTraveler
        fields = ['gender', 'birth_date', 'nationality', 'bio', 'phone']


class FormProfileHostUpdate(forms.ModelForm):
    class Meta:
        model = ProfileHost
        fields = ['name', 'type', 'description', 'phone']

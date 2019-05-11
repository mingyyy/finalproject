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
    phone = PhoneNumberField(widget=forms.TextInput(attrs={}), label='Phone Number', required=False)
    birth_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = ProfileTraveler
        fields = ['gender', 'birth_date', 'nationality', 'phone', 'bio', 'photo', ]
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us more about yourself.'},),

                    }


class FormProfileHostUpdate(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                             label="Phone number", required=False)

    class Meta:
        model = ProfileHost
        fields = ['name', 'type', 'phone', 'description', 'address', 'photo', ]
        widgets = {'description': forms.Textarea(attrs={'placeholder': 'Tell us more about organization.'})}


class FormProfileTravelerUpdate2(forms.ModelForm):

    class Meta:
        model = ProfileTraveler
        fields = ['language']


class FormProfileHostUpdate2(forms.ModelForm):

    class Meta:
        model = ProfileHost
        fields = ['interest', 'interest_details']

from django import forms
from .models import User, Language, ProfileTraveler, ProfileHost
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from django.db import transaction
from ktag.fields import TagField
from .constants import SUBJECT_LIST


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


class FormProfileTravelerUpdate2(forms.ModelForm):
    SUBJECT_LIST.sort(reverse=True)
    expertise = TagField(label='Area of expertise:', delimiters=',', data_list=SUBJECT_LIST,
                         initial='Education', max_tags=8, help_text="Not more than 8 tags please.")
    class Meta:
        model = ProfileTraveler
        fields = ['expertise', 'language', 'experience', 'link']


class FormLanguage(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language',]
        widgets = {'language': forms.Textarea(attrs={'help_text': 'Language you master professionally.'})}
        lables = {'language': 'Language'}


class FormProfileHostUpdate(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                             label="Phone number", required=False)

    class Meta:
        model = ProfileHost
        fields = ['name', 'type', 'phone', 'description', 'address', 'photo', ]
        widgets = {'description': forms.Textarea(attrs={'placeholder': 'Tell us more about your organization.'})}


class FormProfileHostUpdate2(forms.ModelForm):

    class Meta:
        model = ProfileHost

        fields = ['interest', 'interest_details']

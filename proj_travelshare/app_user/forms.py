from django import forms
from .models import User, Language, ProfileTraveler, ProfileHost
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from django.db import transaction
from ktag.fields import TagField
from .constants import SUBJECT_LIST, LANGUAGE_LIST
from django_google_maps.widgets import GoogleMapsAddressWidget

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
    birth_date = forms.DateField(input_formats=['%Y/%m/%d'])

    class Meta:
        model = ProfileTraveler
        fields = ['gender', 'birth_date', 'nationality', 'phone']


class FormProfileTravelerUpdate2(forms.ModelForm):
    languages = TagField(label='Language', delimiters=',', data_list=LANGUAGE_LIST, initial='English')

    class Meta:
        model = ProfileTraveler
        fields = ['bio', 'experience', 'languages', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us more about yourself.'}, ),
            'experience': forms.Textarea(attrs={'placeholder': 'Tell us more about your professional experience.'},),
                    }

    # def save(self):
    #     ProfileTraveler = self.instance
    #     ProfileTraveler.bio = self.cleaned_data['bio']
    #     ProfileTraveler.experience = self.cleaned_data['experience']
    #     language_0 = forms.ChoiceField(choices=LANGUAGE_LIST)
    #     language_1 = forms.ChoiceField(choices=LANGUAGE_LIST)
    #     language_2 = forms.ChoiceField(choices=LANGUAGE_LIST)
    #
    #     language = forms.ModelMultipleChoiceField(queryset=Language.objects.all())
    #     ProfileTraveler.language_set.all().delete()
    #     for i in range(3):
    #         language = self.cleaned_data[f'language_{format(i)}']
    #         ProfileTraveler.objects.create(languages=language)


class FormLanguage(forms.ModelForm):
    language = TagField(label='Language:', delimiters=',', data_list=LANGUAGE_LIST, initial='English')

    class Meta:
        model = ProfileTraveler
        fields = ['language',]
        widgets = {'language': forms.Textarea(attrs={'help_text': 'Only languages you master professionally.'})}
        labels = {'language': 'Languages'}


class FormProfileHostUpdate(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Phone'}),
                             label="Phone number", required=False)

    class Meta:
        model = ProfileHost
        fields = ['photo', 'name', 'type', 'phone', 'description', 'address', 'geolocation']
        labels = {'photo': "Profile photo",
                  'name': "Organization Name",
                  'type': "Organization Type",
                  }
        widgets = {"address": GoogleMapsAddressWidget,
            "geolocation": forms.TextInput(attrs={'placeholder': 'To be filled automatically.',}),
            'description': forms.Textarea(attrs={'placeholder': 'Tell us more about your organization.'})
                   }


class FormAddress(forms.ModelForm):
    class Meta:
        model = ProfileHost
        fields = ['address', 'geolocation',]
        widgets = {
            "address": GoogleMapsAddressWidget,
            "geolocation": forms.TextInput(attrs={'placeholder': 'To be filled automatically.',
                                                 'rows': 1,
                                                 'cols': 10, })

        }


class FormProfileHostUpdate2(forms.ModelForm):

    class Meta:
        model = ProfileHost
        fields = ['interests', 'interest_details']

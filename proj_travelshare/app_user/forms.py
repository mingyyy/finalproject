from django import forms
from .models import User, Language, ProfileTraveler, ProfileHost, Space, Program, Topic
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from django.db import transaction
from ktag.fields import TagField
from .constants import SUBJECT_LIST, LANGUAGE_LIST, SUBJECT_CHOICE
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
    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all())

    class Meta:
        model = ProfileTraveler
        fields = ['bio', 'experience', 'languages', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us more about yourself.'}, ),
            'experience': forms.Textarea(attrs={'placeholder': 'Tell us your professional experience.'},),
                    }


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


# class FormProfileHostUpdate2(forms.ModelForm):
#     LANGUAGE_LIST.sort(reverse=True)
#     SUBJECT_LIST.sort(reverse=True)
#     languages = TagField(label='Language', delimiters=',', data_list=LANGUAGE_LIST, initial='English')
#     interests = TagField(label="Topics of your interest", delimiters=',', data_list=SUBJECT_LIST, initial='Education')
#
#     class Meta:
#         model = ProfileHost
#         fields = ['interests', 'interest_details',  'languages']
#         labels = {'interest_details': "Detail of your interests",
#                   }
#         widgets = {'languages': forms.Textarea(attrs={'help_text': 'Languages you need for the event.'})
#                    }


class FormProfileHostUpdate2(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField(queryset=Language.objects.all())
    interests = forms.ModelMultipleChoiceField(queryset=Topic.objects.all())

    class Meta:
        model = ProfileHost
        fields = ['interests', 'interest_details', 'languages']
        labels = {'interests': "Subjects of interest",
                  'interest_details': "Tell us more about your interests",
                  }
        widgets = {'languages': forms.Textarea(attrs={'help_text': 'Languages you need for the event.'}),
                   }


class FormSpace(forms.ModelForm):
    class Meta:
        model = Space
        fields = ['title', 'detail']
        label = {'title': "What you offer"}
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Meeting room for 50 people',}),
            'detail': forms.Textarea(attrs={'placeholder': 'Details of the space, equipments etc',}),
        }


class FormProgram(forms.ModelForm):
    # SUBJECT_LIST.sort(reverse=True)
    # subject = TagField(label='Subject', delimiters=',', data_list=SUBJECT_LIST, initial='Education')

    subject = forms.ModelMultipleChoiceField(queryset=Topic.objects.all())
    class Meta:
        model = Program
        fields = ['subject', 'type', 'frequency', 'duration', 'title', 'description', 'requirement']
        labels = {'type': "Type of event",
                  }


class DeleteProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = []


class DeleteSpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = []


# testing address
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
from .models import Trip
from django import forms


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ["user",]
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_date': forms.DateInput(),
            'end_date': forms.DateInput(),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%Y-%m-%d',)
        self.fields['end_date'].input_formats = ('%Y-%m-%d',)


class TripDeleteForm(forms.Form):
    confirm = forms.CharField(max_length=7, widget=forms.Textarea(attrs={'placeholder': 'confirm', 'rows': 1, 'cols': 4}),
                        required=False, label='')
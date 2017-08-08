from django import forms
from .models import Activity, TimeSpend


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'type', ]


class TimeSpendForm(forms.ModelForm):
    class Meta:
        model = TimeSpend
        fields = ['date', 'duration']
        labels = {'duration': 'add duration in hours:'}
        widgets = {'duration': forms.TimeInput(format='%H:%M'),
                   'date': forms.SelectDateWidget(),
                   }

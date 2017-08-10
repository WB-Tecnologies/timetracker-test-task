from django import forms
from .models import Activity, TimeSpend


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'type', ]


class TimeSpendForm(forms.ModelForm):
    class Meta:
        model = TimeSpend
        fields = ['date', 'time_spent']
        labels = {'time_spent': 'add duration in hours:'}
        widgets = {'time_spent': forms.NumberInput(),
                   'date': forms.SelectDateWidget(),
                   }

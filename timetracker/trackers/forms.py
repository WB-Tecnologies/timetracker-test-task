from django import forms
from .models import Activity, TimeSpend


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', "TYPE_CHOICES", ]

    def set_owner(self, request):
        new_activity = self.save(commit=False)
        new_activity.owner = request.user


class TimeSpendForm(forms.ModelForm):
    class Meta:
        model = TimeSpend
        fields = ['date', 'time_spent']
        labels = {'time_spent': 'add duration in hours:'}
        widgets = {'time_spent': forms.NumberInput(),
                   'date': forms.SelectDateWidget(),
                   }

    def set_activity(self, activity):
        new_time_spend = self.save(commit=False)
        new_time_spend.activity = activity

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Activity(models.Model):
    """a business that makes user))"""
    title = models.CharField(max_length=30)
    type = models.CharField(
        max_length=1, choices=(('W', 'work'), ('O', 'other')), default='W')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def total_duration(self):
        total_duration_sum = self.activity_time_spend.all().aggregate(Sum('time_spent'))
        return total_duration_sum['time_spent__sum']

    # def time_spend_list(self):
    #     return self.activity_time_spend.all()

    def __str__(self):
        return self.title


class TimeSpend(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='activity_time_spend'
    )
    date = models.DateTimeField()
    time_spent = models.PositiveIntegerField()

    @staticmethod
    def work_activity_time_sum():
        time_sum = TimeSpend.objects.filter(activity__type='W')\
            .aggregate(Sum('time_spent'))
        return time_sum['time_spent__sum']

    @staticmethod
    def other_activity_time_sum():
        time_sum = TimeSpend.objects.filter(activity__type='O') \
            .aggregate(Sum('time_spent'))
        return time_sum['time_spent__sum']
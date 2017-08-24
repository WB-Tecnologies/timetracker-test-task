from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Activity(models.Model):
    """a business that makes user))"""
    WORK_VALUE = 'W'
    WORK_LABEL = 'work'
    OTHER_VALUE = 'O'
    OTHER_LABEL = 'other'

    title = models.CharField(max_length=30)
    TYPE_CHOICES = models.CharField(
        max_length=1, choices=((WORK_VALUE, WORK_LABEL), (OTHER_VALUE, OTHER_LABEL)), default='W')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = "Activities"

    def total_duration(self):
        total_duration_sum = self.activity_time_spend.all().aggregate(Sum('time_spent'))
        return total_duration_sum['time_spent__sum']

    def __str__(self):
        return self.title


class TimeSpend(models.Model):
    """ time spent on activities by dates"""
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, related_name='activity_time_spend')
    date = models.DateTimeField()
    time_spent = models.PositiveIntegerField()

    def work_activity_time_sum(self, user):
        time_sum = TimeSpend.objects.filter(activity__owner=user).\
            filter(activity__TYPE_CHOICES=Activity.WORK_VALUE).aggregate(Sum('time_spent'))
        return time_sum['time_spent__sum']

    def other_activity_time_sum(self, user):
        time_sum = TimeSpend.objects.filter(activity__owner=user).\
            filter(activity__TYPE_CHOICES=Activity.OTHER_VALUE).aggregate(Sum('time_spent'))
        return time_sum['time_spent__sum']

    def all_activity_time(self, user):
        time_sum = TimeSpend.objects.filter(activity__owner=user).aggregate(Sum('time_spent'))
        return time_sum['time_spent__sum']

    def percentage(self, user):
        other = self.other_activity_time_sum(user)
        work = self.work_activity_time_sum(user)

        if work and other:
            result = work * 100 / (work + other)
            return float("{0:.1f}".format(result))
        elif work:
            return 100
        else:
            return 0

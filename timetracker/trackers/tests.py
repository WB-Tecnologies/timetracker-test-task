from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Activity, TimeSpend


class ActivityTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test', password='test123')
        activity_w = Activity.objects.create(title='testW', type='W', owner=user)
        activity_o = Activity.objects.create(title='testO', type='O', owner=user)
        TimeSpend.objects.create(activity=activity_w,
                                 date=timezone.now(), time_spent=1)
        TimeSpend.objects.create(activity=activity_w,
                                 date=timezone.now(), time_spent=1)
        TimeSpend.objects.create(activity=activity_o,
                                 date=timezone.now(), time_spent=1)

    def test_activity_time_sum(self):
        """ test """
        user = User.objects.get(username='test')
        activity = Activity.objects.get(title='testW')
        self.assertEqual(Activity.total_duration(activity), 2)
        self.assertEqual(TimeSpend.work_activity_time_sum(user), 2)
        self.assertEqual(TimeSpend.other_activity_time_sum(user), 1)

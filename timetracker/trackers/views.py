from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from .models import Activity, TimeSpend
from .forms import ActivityForm, TimeSpendForm

time = TimeSpend()


def check_owner(request, activity):
    if activity.owner != request.user:
        raise Http404


@login_required()
def index(request):
    """homepage with activities"""
    activities = Activity.objects.filter(owner=request.user).order_by('date_added')
    user = request.user
    work_statistic = time.work_activity_time_sum(user)
    other_statistic = time.other_activity_time_sum(user)
    percentage_w_to_all = time.percentage(user)
    all_time = time.all_activity_time(user)
    return render(request, 'trackers/index.html', {
        'activities': activities,
        'work_statistic': work_statistic,
        'other_statistic': other_statistic,
        'percentage_w_to_all': percentage_w_to_all,
        'all_time': all_time,
    })


class ActivityCreate(FormView):
    template_name = 'trackers/add_activity.html'
    form_class = ActivityForm

    def form_valid(self, form):
        form.set_owner(self.request)
        form.save()
        return HttpResponseRedirect(reverse('trackers:index'))


@login_required()
def add_duration(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    check_owner(request, activity)
    if request.method == 'POST':
        form = TimeSpendForm(request.POST)
        if form.is_valid():
            form.set_activity(activity)
            form.save()
            return HttpResponseRedirect(reverse('trackers:index'))
    else:
        form = TimeSpendForm()

    return render(request, 'trackers/add_duration.html', {'activity': activity, 'form': form})

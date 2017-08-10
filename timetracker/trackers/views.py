from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Activity, TimeSpend
from .forms import ActivityForm, TimeSpendForm


def check_owner(request, activity):
    if activity.owner != request.user:
        raise Http404


def percentage(work, other):
    if work and other:
        result = work * 100 / (work + other)
        return float("{0:.1f}".format(result))
    else:
        if work:
            return 100
        else:
            return 0


@login_required()
def index(request):
    """homepage with activities"""
    activities = Activity.objects.filter(owner=request.user).order_by('date_added')
    work_statistic = TimeSpend.work_activity_time_sum()
    other_statistic = TimeSpend.other_activity_time_sum()
    percentage_w_to_all = percentage(work_statistic, other_statistic)
    return render(request, 'trackers/index.html', {
        'activities': activities,
        'work_statistic': work_statistic,
        'other_statistic': other_statistic,
        'percentage_w_to_all': percentage_w_to_all
    })


@login_required()
def add_activity(request):
    if request.method != 'POST':
        form = ActivityForm()
    else:
        form = ActivityForm(request.POST)
        if form.is_valid():
            new_activity = form.save(commit=False)
            new_activity.owner = request.user
            new_activity.save()
            return HttpResponseRedirect(reverse('trackers:index'))

    context = {'form': form}
    return render(request, 'trackers/add_activity.html', context)


def add_duration(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id)
    check_owner(request, activity)
    if request.method != 'POST':
        form = TimeSpendForm()
    else:
        form = TimeSpendForm(request.POST)
        if form.is_valid():
            new_time_spend = form.save(commit=False)
            new_time_spend.activity = activity
            new_time_spend.save()
            return HttpResponseRedirect(reverse('trackers:index'))

    return render(request, 'trackers/add_duration.html', {'activity': activity,
                                                          'form': form})

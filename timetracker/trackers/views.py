from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Activity
from .forms import ActivityForm, TimeSpendForm


def check_owner(request, activity):
    if activity.owner != request.user:
        raise Http404


@login_required()
def index(request):
    """homepage with activities"""
    activities = Activity.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'trackers/index.html', {'activities': activities})


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

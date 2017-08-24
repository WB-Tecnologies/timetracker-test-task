from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_activity/$', login_required(views.ActivityCreate.as_view()), name='add_activity'),
    url(r'^add_duration/(?P<activity_id>\d+)/$', views.add_duration,
        name='add_duration'),
]

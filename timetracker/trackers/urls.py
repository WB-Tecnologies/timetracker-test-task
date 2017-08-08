from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_activity/$', views.add_activity, name='add_activity'),
    url(r'^add_duration/(?P<activity_id>\d+)/$', views.add_duration,
        name='add_duration'),
]

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^main/$', views.main, name='main'),
    url(r'^process/$', views.process, name='process'),
    url(r'^login/$', views.login, name='login'),
    url(r'^travels/$', views.traveldash, name='travels'),
    url(r'^travels/add/$', views.add, name='add'),
    url(r'^travels/verify/$', views.verify, name='verify'),
    url(r'^travels/destination/(?P<id>\d+)/$', views.destination, name='destination'),
    url(r'^travels/join/(?P<id>\d+)/$', views.join, name='join'),
    url(r'^logout/$', views.logout, name='logout'),
]

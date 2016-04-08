from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html', views.index, name='index'),
    url(r'^dashboard.html', views.dashboard, name='dashboard'),
    url(r'^statistics.html', views.statistics, name='statistics'),
    url(r'^task.html', views.task, name='task')
]
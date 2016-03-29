from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index.html', views.index, name='index'),
    url(r'^dashboard.html', views.dashboard, name='dashboard'),
    url(r'^charts.html', views.charts, name='charts'),
    url(r'^tables.html', views.tables, name='tables'),
]
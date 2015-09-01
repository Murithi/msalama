from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from . import views

urlpatterns = patterns('',
                       url('^data/$', views.GraphDataView.as_view(), name='data'),
                       url(r'^$', TemplateView.as_view(template_name='dashboard.html'), name="dashboard"),
                       )

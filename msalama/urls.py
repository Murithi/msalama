from django.conf.urls import include, url
from django.contrib import admin
from msalamaclient import views
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    # Examples:
     url(r'^$', 'msalamaclient.views.login', name='login'),
     url(r'^appointments/$', views.AppointmentListView.as_view(), name='appointment_list'),
     url(r'^messages/$', 'msalamaclient.views.Messages', name="message_list"),
     url(r'^sendmessage/$', views.SendMessageFormView.as_view(), name="sendmessage"),
     url(r'^vaccinereceived/$', views.VaccineReceivedReportView.as_view(), name='vaccinereceived'),
     url(r'^vaccinelist/$', 'msalamaclient.views.vaccinelist', name='vaccinelist'),
     url(r'^login', 'msalamaclient.views.login', name='login'),
     url(r'^auth', 'msalamaclient.views.auth_view', name='auth'),
     url(r'^logout', 'msalamaclient.views.logout', name='logout'),
     url(r'^loggedin', 'msalamaclient.views.loggedin', name='loggedin'),
     url(r'^invalid', 'msalamaclient.views.invalid_login', name='invalid'),
     url(r'^signup/$', 'msalamaclient.views.signup', name='signup'),
     url(r'^signup_success$', 'msalamaclient.views.signup_success', name='signup_success'),
     url(r'^userprofile$', 'msalamaclient.views.userprofile', name='userprofile'),
     url(r'^vaccines$', 'msalamaclient.views.vaccines',name='vaccines'),
     url(r'^childvaccines$', 'msalamaclient.views.childvaccines',name='childvaccines'),
     url(r'^polio$', 'msalamaclient.views.polio',name='polio'),
    url(r'^reportvaccine$', 'msalamaclient.views.reportvaccine',name='reportvaccine'),
    url(r'^makeappointment$', views.MakeAppointmentFormView.as_view(), name='makeappointment'),
    url(r'^updatevaccine/$', 'msalamaclient.views.updatevaccine', name='updatevaccine'),
    url(r'^updatevaccineview/$', 'msalamaclient.views.updatevaccineview', name='updatevaccineview'),

    url(r'^images/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^dashboard/', include('msalamaclient.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
]
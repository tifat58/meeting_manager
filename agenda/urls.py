__author__ = 'Tusfiqur'

from django.conf.urls import include, url
from django.contrib import admin
from agenda import views
from agenda.views import AgendaView

urlpatterns = [

    url(r'test/$', views.test, name="test"),
    url(r'^meetingAdd/$', views.add_meeting, name="new_meeting"),
    url(r'^agendaAdd/$', views.add_agenda, name="new_agenda"),
    url(r'^agendaList/$', views.view_agenda_list, name="agenda_list"),
    url(r'^(?P<agenda_id>[0-9]+)/agendaDetail/$', views.agenda_detail, name="agenda_detail_view"),
    url(r'^(?P<agenda_id>[0-9]+)/edit_agenda/$', views.edit_agenda, name="edit_agenda"),
    url(r'^(?P<member_id>[0-9]+)/(?P<agenda_id>[0-9]+)/add_remarks/$', views.add_remarks, name="remarks_add"),
    url(r'^(?P<meeting_id>[0-9]+)/meeting_dashboard/$', views.meeting_dashboard, name="meeting_dashboard"),
    url(r'^archive/$', views.meeting_archive, name="archive"),
    url(r'^(?P<agenda_id>[0-9]+)/agenda_archive/$', views.agenda_detail_view_mode, name="agenda_archive"),

]
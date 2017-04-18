__author__ = 'Tusfiqur'

from django.conf.urls import include, url
from django.contrib import admin
from company import views

urlpatterns = [

    url(r'^companyAdd/$', views.add_company, name="new_company"),
    url(r'^designationAdd/$', views.add_designation, name="new_designation"),
    url(r'^companyMemberAdd/$', views.add_company_member, name="new_member"),
    url(r'^memberDetails/$', views.add_member_details, name="member_details"),

]
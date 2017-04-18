__author__ = 'Tusfiqur'
from django.conf.urls import include, url
from django.contrib import admin
from account import views

urlpatterns = [
    url(r'^create_user/$', views.add_user, name="add_user"),
    url(r'^create_usergroup/$', views.add_user_group, name="add_group"),
    url(r'^add_menu/$', views.add_menu, name="add_menu"),
    url(r'^change_password/$', views.change_password, name="change_password"),

]

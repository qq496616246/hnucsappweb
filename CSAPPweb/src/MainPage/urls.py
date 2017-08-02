#coding=UTF-8
from django.conf.urls import url
from MainPage import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^test$', views.test),
]

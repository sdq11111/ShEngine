from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^init/$', views.init),
    url(r'^page/$', views.page),
    url(r'^pub/$', views.pub),
]
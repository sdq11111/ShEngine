from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^page/$', views.page),
    url(r'^pub/$', views.pub),
]
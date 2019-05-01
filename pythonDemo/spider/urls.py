from django.urls import path

from . import views

urlpatterns = [
    path(r'index', views.index, name='index'),
    path(r'pie', views.getBrandPie, name='pie'),
    path(r'bar', views.getBrandBar, name='bar'),
    path(r'parseVideo', views.getParseVideo, name='parseVideo'),
]
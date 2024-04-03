from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("",views.query_view, name="index"),
    re_path(r'^list/$',views.query_view, name='list'),
]
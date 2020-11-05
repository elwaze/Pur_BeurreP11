from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^connection$', views.connection, name='connection'),
    re_path(r'^disconnection$', views.disconnection, name='disconnection'),
    re_path(r'^create_account$', views.create_account, name='create_account'),
    re_path(r'^my_account$', views.my_account, name='my_account'),

]

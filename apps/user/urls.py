from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^connection$', views.connection, name='connection'),
    re_path(r'^disconnection$', views.disconnection, name='disconnection'),
    re_path(r'^create_account$', views.create_account, name='create_account'),
    re_path(r'^my_account$', views.my_account, name='my_account'),
    # re_path(r'^user_confirmation$', views.user_confirmation, name='user_confirmation'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]

from django.urls import path
# from django.conf.urls import url
from . import views


urlpatterns = [
    path('connection', views.connection, name='connection'),
    path('disconnection', views.disconnection, name='disconnection'),
    path('create_account', views.create_account, name='create_account'),
    path('my_account', views.my_account, name='my_account'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('home', views.home, name='homepage'),
    path('legal_notices', views.legal_notices, name='legal')
]
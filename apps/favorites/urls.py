from django.urls import path
from . import views

urlpatterns = [
    path('favorites', views.favorites, name='favorites'),
    path('save', views.save, name='save'),
    path('remove', views.remove, name='remove'),
]

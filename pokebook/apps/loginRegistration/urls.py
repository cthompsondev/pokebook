from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('users/create', views.users_create),
    path('users/<int:id>', views.users_show),
    path('users/login', views.users_login),
    path('logout',views.logout),
    path('ajax/validate_email/', views.validate_email, name='validate_email'),
    path('users/<int:id>/pokes', views.poke_show),
    path('users/<int:id>/poke', views.poke_create)
]

from django.urls import path

from . import views


app_name = 'user_profile'

urlpatterns = [
    path('', views.ProfileUpdateView.as_view(), name='profile'),
]
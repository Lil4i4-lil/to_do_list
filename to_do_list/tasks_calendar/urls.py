from django.urls import path

from . import views


app_name = 'tasks_calendar'


urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.daily_tasks_redirect, name='daily_tasks'),
]
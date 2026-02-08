from django.urls import path

from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('<int:id>/', views.task, name='task'),
    path('add_task/', views.add_task, name='add_task'),
    path('<int:id>/confirm-delete/', views.confirm_delete, name='confirm_delete'),
]
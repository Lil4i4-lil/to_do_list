from django.urls import path

from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('<int:id>/', views.TaskUpdateView.as_view(), name='task'),
    path('add_task/', views.TaskCreateView.as_view(), name='add_task'),
    path('<int:id>/confirm-delete/', views.confirm_delete, name='confirm_delete'),
]
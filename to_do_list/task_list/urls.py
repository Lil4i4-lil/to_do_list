from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', views.TaskUpdateView.as_view(), name='task'),
    path('add_task/', views.TaskCreateView.as_view(), name='add_task'),
    path('<int:pk>/confirm-delete/',
         views.TaskDeleteView.as_view(),
         name='confirm_delete'),
]
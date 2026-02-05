from django.shortcuts import render

from .models import Task
from .forms import TaskForm


def task_list(request):
    user_id = request.user.id
    context = {"tasks": Task.objects.filter(author_id=user_id).order_by("created_at")}
    template = "task_list/task_list.html"
    return render(request, template, context)

def task(request):
    form = TaskForm()
    context = {"form": form}
    template = "task_list/task.html"
    return render(request, template, context)

def add_task(request):
    form = TaskForm()
    context = {"form": form}
    template = "task_list/add_task.html"
    return render(request, template, context)

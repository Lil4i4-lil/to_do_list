from django.shortcuts import render, get_object_or_404

from .models import Task
from .forms import TaskForm


def task_list(request):
    user_id = request.user.id
    context = {"tasks": Task.objects.filter(author_id=user_id).order_by("created_at")}
    template = "task_list/task_list.html"
    return render(request, template, context)

def task(request, id):
    task_info = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task_info)
    context = {"form": form, "task": task, "title": "Ваша заметка"}
    template = "task_list/task_info.html"
    return render(request, template, context)

def add_task(request):
    form = TaskForm()
    context = {"form": form, "title": "Создание новой заметки"}
    template = "task_list/task_info.html"
    return render(request, template, context)

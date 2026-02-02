from django.shortcuts import render

from .forms import TaskForm


def task_list(request):
    template = "task_list/task_list.html"
    return render(request, template)

def add_task(request):
    form = TaskForm()
    context = {"form": form}
    template = "task_list/add_task.html"
    return render(request, template, context)

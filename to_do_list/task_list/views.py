from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .models import Task
from .forms import TaskForm


def task_list(request):
    user_id = request.user.id
    tasks = Task.objects.filter(author_id=user_id).order_by("created_at")
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    template = "task_list/task_list.html"
    return render(request, template, context)

def task(request, id):
    instance = get_object_or_404(Task, pk=id)
    form = TaskForm(request.POST or None, instance=instance)

    if "save" in request.POST and form.is_valid():
        form.save()
        return redirect("tasks:task_list")
    elif "cancel" in request.POST:
        return redirect("tasks:task_list")
    elif "complete" in request.POST:
        pass

    context = {"form": form, "task": instance, "title": "Ваша заметка"}
    template = "task_list/edit_task.html"
    return render(request, template, context)

def add_task(request):
    form = TaskForm(request.POST or None)

    if "save" in request.POST and form.is_valid():
        task = form.save(commit=False)
        task.author = request.user
        task.save()
        return redirect("tasks:task_list")
    elif "cancel" in request.POST:
        return redirect("tasks:task_list")

    context = {"form": form, "title": "Создание новой заметки"}
    template = "task_list/add_task.html"
    return render(request, template, context)

def confirm_delete(request, id):
    instance = get_object_or_404(Task, pk=id)

    if "confirm-delete" in request.POST:
        instance.delete()
        return redirect("tasks:task_list")
    else:
        return redirect("tasks:task", id=id)

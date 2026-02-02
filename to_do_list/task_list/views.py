from django.shortcuts import render


def task_list(request):
    template = "task_list/task_list.html"
    return render(request, template)

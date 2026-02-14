from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Task
from .forms import TaskForm


class TaskMixin:
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task_list")


class TaskListView(ListView):
    model = Task
    ordering = "created_at"
    queryset = Task.objects.all().prefetch_related('tags').select_related('author')
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author_id=self.request.user)


class TaskCreateView(TaskMixin, CreateView):
    template_name = "task_list/add_task.html"

    def form_valid(self, form):
        """Обработка валидной формы - добавляем автора"""
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана!')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """Обработка POST с разными кнопками"""
        if 'cancel' in request.POST:
            return redirect(self.success_url)

        return super().post(request, *args, **kwargs)


class TaskUpdateView(TaskMixin, UpdateView):
    template_name = "task_list/edit_task.html"

    def get_object(self, queryset=None):
        """Получаем объект задачи по id из URL"""
        id = self.kwargs.get('id')
        return get_object_or_404(Task, pk=id)

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса с разными кнопками"""
        self.object = self.get_object()

        if 'cancel' in request.POST:
            return redirect('tasks:task_list')
        elif 'complete' in request.POST:
            pass
        elif 'save' in request.POST:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        return redirect('tasks:task_list')


def confirm_delete(request, id):
    instance = get_object_or_404(Task, pk=id)

    if "confirm-delete" in request.POST:
        instance.delete()
        return redirect("tasks:task_list")
    else:
        return redirect("tasks:task", id=id)

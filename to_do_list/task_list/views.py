from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


class TaskMixin:
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task_list")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10
    tag = None
    queryset = (Task.objects.all()
                .prefetch_related('tags')
                .select_related('author')
                .order_by('created_at'))

    def get_queryset(self):
        queryset = super().get_queryset().filter(completed=False)

        self.tag = self.request.GET.get('tag', '')

        if self.tag:
            queryset = queryset.filter(tags__tag__icontains=self.tag)

        return queryset.filter(author_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = self.queryset.filter(completed=True)
        context['tag'] = getattr(self, 'tag', '')
        return context


class TaskCreateView(TaskMixin, LoginRequiredMixin, CreateView):
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


class TaskUpdateView(TaskMixin, LoginRequiredMixin, UpdateView):
    template_name = "task_list/edit_task.html"

    def get_queryset(self):
        queryset = Task.objects.all().prefetch_related('tags').select_related('author')
        return queryset.filter(author_id=self.request.user)

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса с разными кнопками"""
        self.object = self.get_object()

        if 'cancel' in request.POST:
            return redirect('tasks:task_list')
        elif 'complete' in request.POST:
            self.object.completed = True
            self.object.save()
            return redirect('tasks:task_list')
        elif 'save' in request.POST:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        return redirect('tasks:task_list')


class TaskDeleteView(TaskMixin, LoginRequiredMixin, DeleteView):
    template_name = "task_list/edit_task.html"

    def get_queryset(self):
        queryset = Task.objects.all().prefetch_related('tags').select_related('author').order_by('created_at')
        return queryset.filter(author_id=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "confirm-delete" in request.POST:
            self.object.delete()
            return redirect(self.success_url)
        else:
            return redirect("tasks:task", pk=self.object.pk)



def confirm_delete(request, pk):
    instance = get_object_or_404(Task, pk=pk)

    if "confirm-delete" in request.POST:
        instance.delete()
        return redirect("tasks:task_list")
    else:
        return redirect("tasks:task", pk=pk)

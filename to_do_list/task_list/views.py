from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TaskForm
from .models import Task


class TaskMixin:
    model = Task
    form_class = TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    queryset = (Task.objects.all()
                .prefetch_related('tags')
                .select_related('author'))
    paginate_by = 20
    tag = None
    order = 'created_at'
    selected_date = None

    def get_queryset(self):
        queryset = super().get_queryset().filter(completed=False)

        date_param = self.request.GET.get('date')
        if date_param:
            try:
                selected_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(planned_date=selected_date)
                self.selected_date = selected_date
            except (ValueError, TypeError):
                pass

        match self.request.GET.get('sort', ''):
            case 'date_desc':
                self.order = '-created_at'
            case 'planned_date_asc':
                self.order = 'planned_date'
            case 'planned_date_desc':
                self.order = '-planned_date'
            case 'name_asc':
                self.order = 'title'
            case 'name_desc':
                self.order = '-title'
            case _:
                self.order = 'created_at'

        queryset = queryset.order_by(self.order)

        self.tag = self.request.GET.get('tag', '')

        if self.tag:
            queryset = queryset.filter(tags__tag__icontains=self.tag)

        return queryset.filter(author_id=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = self.queryset.filter(completed=True).order_by('-completion_date')
        context['tag'] = getattr(self, 'tag', '')
        context['order'] = getattr(self, 'order', '')
        context['today'] = date.today()

        if self.selected_date:
            context['selected_date'] = self.selected_date
            context['date_title'] = self.selected_date.strftime('%d %B %Y')
            context['date_param'] = self.request.GET.get('date')

        return context


class TaskCreateView(TaskMixin, LoginRequiredMixin, CreateView):
    template_name = "task_list/add_task.html"
    date_from_calendar = None
    # success_url = reverse_lazy('tasks:task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def get_initial(self):
        initial = super().get_initial()
        date_param = self.request.GET.get('date')

        if date_param:
            try:
                planned_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                initial['planned_date'] = planned_date
                self.request.session['return_date'] = date_param
            except (ValueError, TypeError):
                pass

        return initial

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')

        if next_url:
            return next_url

        if self.object and self.object.planned_date:
            return reverse('tasks:task_list') + f'?date={self.object.planned_date}'

        return reverse('tasks:task_list')

    def form_valid(self, form):
        """Обработка валидной формы - добавляем автора"""

        if form.instance.planned_date and form.instance.planned_date < timezone.now().date():
            form.add_error('planned_date', 'Дата выполнения не может быть в прошлом')
            return super().form_invalid(form)
        elif not form.instance.planned_date:
            form.instance.planned_date = timezone.now().date()

        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана!')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        """Обработка POST с разными кнопками"""
        if 'cancel' in request.POST:
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('tasks:task_list')

        return super().post(request, *args, **kwargs)


class TaskUpdateView(TaskMixin, LoginRequiredMixin, UpdateView):
    template_name = "task_list/edit_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def get_queryset(self):
        queryset = (Task.objects.all()
                    .prefetch_related('tags')
                    .select_related('author'))

        return queryset.filter(author_id=self.request.user)

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')

        if next_url:
            return next_url

        if self.object and self.object.planned_date:
            return reverse('tasks:task_list') + f'?date={self.object.planned_date}'

        return reverse('tasks:task_list')

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса с разными кнопками"""
        self.object = self.get_object()
        next_url = self.request.POST.get('next') or self.request.GET.get('next')

        if 'cancel' in request.POST:
            if next_url:
                return redirect(next_url)
            return redirect('tasks:task_list')
        elif 'complete' in request.POST:
            self.object.completed = True
            self.object.completion_date = date.today()
            self.object.save()
            if next_url:
                return redirect(next_url)
            return redirect('tasks:task_list')
        elif 'save' in request.POST:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        return redirect('tasks:task_list')

    def form_valid(self, form):
        """Обработка валидной формы - добавляем автора"""
        if form.instance.planned_date < timezone.now().date():
            form.add_error('planned_date', 'Дата выполнения не может быть в прошлом')
            return super().form_invalid(form)

        return super().form_valid(form)


class TaskDeleteView(TaskMixin, LoginRequiredMixin, DeleteView):
    template_name = "task_list/edit_task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def get_queryset(self):
        queryset = (Task.objects.all()
                    .prefetch_related('tags')
                    .select_related('author')
                    .order_by('created_at'))
        return queryset.filter(author_id=self.request.user)

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')

        if next_url:
            return next_url

        if self.object and self.object.planned_date:
            return reverse('tasks:task_list') + f'?date={self.object.planned_date}'

        return reverse('tasks:task_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if "confirm-delete" in request.POST:
            self.object.delete()
            return redirect(self.get_success_url())
        else:
            return redirect("tasks:task", pk=self.object.pk)



def confirm_delete(request, pk):
    instance = get_object_or_404(Task, pk=pk)
    next_url = request.POST.get('next') or request.GET.get('next')

    if "confirm-delete" in request.POST:
        planned_date = instance.planned_date
        instance.delete()
        if next_url:
            return redirect(next_url)
        elif planned_date:
            return redirect(reverse('tasks:task_list') + f'?date={planned_date}')
        else:
            return redirect('tasks:task_list')
    else:
        return redirect("tasks:task", pk=pk)

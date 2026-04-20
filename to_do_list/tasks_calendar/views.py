import calendar
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from task_list.models import Task


@login_required
def calendar_view(request, year=None, month=None):
    if not year:
        year = timezone.now().year
    if not month:
        month = timezone.now().month

    tasks = Task.objects.filter(
        author_id=request.user,
        planned_date__year=year,
        planned_date__month=month
    )

    today = date.today()
    for task in tasks:
        task.is_overdue = (not task.completed and
                           task.planned_date and
                           task.planned_date < today)

    cal = calendar.monthcalendar(year, month)

    # Вычисляем предыдущий и следующий месяц для навигации
    first_day_of_month = datetime(year, month, 1)
    prev_month = first_day_of_month - timedelta(days=1)
    next_month = first_day_of_month + timedelta(days=32)

    context = {
        'cal': cal,
        'tasks': tasks,  # Передаем все задачи напрямую
        'month': month,
        'year': year,
        'prev_month': prev_month,
        'next_month': next_month,
        'current_date': first_day_of_month,
    }

    return render(request, 'tasks_calendar/calendar.html', context)


@login_required
def daily_tasks_redirect(request, year, month, day):
    """Редирект на страницу списка задач с фильтром по дате"""
    selected_date = f"{year}-{month:02d}-{day:02d}"

    print(f"Перенаправление на дату: {selected_date}")
    print(f"URL: {reverse('tasks:task_list')}?date={selected_date}")

    return redirect(f"{reverse('tasks:task_list')}?date={selected_date}")

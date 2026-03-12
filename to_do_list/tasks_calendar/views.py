import calendar
from datetime import date, datetime, timedelta
from django.shortcuts import render
from django.utils import timezone

from task_list.models import Task


def calendar_view(request, year=None, month=None):
    if not year:
        year = timezone.now().year
    if not month:
        month = timezone.now().month

    tasks = Task.objects.filter(
        author_id=request.user,
        created_at__year=year,
        created_at__month=month
    )

    tasks_by_day = {}
    for task in tasks:
        day = task.created_at.day
        if day not in tasks_by_day:
            tasks_by_day[day] = []
        tasks_by_day[day].append(task)

    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    prev_month = datetime(year, month, 1) - timedelta(days=1)
    next_month = datetime(year, month, 28) + timedelta(days=4)
    current_date = datetime(year, month, 1)

    context = {
        'cal': cal,
        'tasks_by_day': tasks_by_day,
        'month_name': month_name,
        'year': year,
        'prev_month': prev_month,
        'next_month': next_month,
        'today': date.today(),
        'current_date': current_date,
    }

    return render(request, 'tasks_calendar/calendar.html', context)

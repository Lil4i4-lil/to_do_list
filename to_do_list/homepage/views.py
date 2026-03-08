from django.views.generic import TemplateView
from task_list.models import Task


class HomePage(TemplateView):
    template_name = 'homepage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user

        if self.request.user.is_authenticated:
            context['task_count'] = (Task.objects
                                     .filter(author_id=self.request.user, completed=0)
                                     .count())
        else:
            context['task_count'] = 0  # или None, или не добавлять вообще

        return context
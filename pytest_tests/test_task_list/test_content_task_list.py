from django.urls import reverse
from pytest_cases import fixture_ref, parametrize
from task_list.forms import TaskForm


@parametrize(
    'client, task_in_list',
    (
        (fixture_ref('author_client'), True),
        (fixture_ref('not_author_client'), False)
    )
)
def test_task_in_list_for_different_users(task, client, task_in_list):
    url = reverse('tasks:task_list')
    response = client.get(url)
    object_list = response.context['object_list']
    assert (task in object_list) == task_in_list


@parametrize(
    'page, args',
    (
        ('tasks:add_task', None),
        ('tasks:task', fixture_ref('task_id'))
    )
)
def test_pages_contains_form(author_client, page, args):
    url = reverse(page, args=args)
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], TaskForm)

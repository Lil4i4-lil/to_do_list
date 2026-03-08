import pytest
from django.test.client import Client
from task_list.models import Task


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Not author')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def task(author):
    task = Task.objects.create(title="Задача",
                               content="Задача 1",
                               author=author
                               )
    return task


@pytest.fixture
def task_id(task):
    return (task.id,)


@pytest.fixture
def task_form_data():
    return {
        'title': 'Новая задача',
        'content': 'Новая задача 1'
    }


@pytest.fixture
def profile_form_data():
    return {
        'username': 'user',
        'email': 'mm@mail.ru',
        'phone_number': '89215554433',
        'first_name': 'Ivan',
        'last_name': 'Antonov',
        'birthday': '2005-12-24'
    }


@pytest.fixture
def author_task_count(author):
    return author.tasks.all().count()

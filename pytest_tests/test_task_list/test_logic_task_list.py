import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_cases import fixture_ref, parametrize
from pytest_django.asserts import assertRedirects

from task_list.models import Task


def test_user_can_create_task(author_client, author, task_form_data):
    url = reverse('tasks:add_task')
    response = author_client.post(url, data=task_form_data)

    assertRedirects(response, reverse('tasks:task_list'))
    assert Task.objects.count() == 1

    new_task = Task.objects.get()

    assert new_task.title == task_form_data['title']
    assert new_task.content == task_form_data['content']
    assert new_task.author == author


@pytest.mark.django_db
def test_anon_user_cant_create_task(client, task_form_data):
    url = reverse('tasks:add_task')
    response = client.post(url, data=task_form_data)

    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'

    assertRedirects(response, expected_url)
    assert Task.objects.count() == 0


def test_author_can_edit_task(author_client, task, task_form_data):
    url = reverse('tasks:task', args=(task.id,))
    task_form_data['save'] = 'Save'
    response = author_client.post(url, task_form_data)

    assertRedirects(response, reverse('tasks:task_list'))

    task.refresh_from_db()

    assert task.title == task_form_data['title']
    assert task.content == task_form_data['content']


def test_not_author_cant_edit_task(not_author_client, task, task_form_data):
    url = reverse('tasks:task', args=(task.id,))
    response = not_author_client.post(url, data=task_form_data)

    assert response.status_code == HTTPStatus.NOT_FOUND

    task_from_db = Task.objects.get(id=task.id)

    assert task.title == task_from_db.title
    assert task.content == task_from_db.content


def test_author_can_delete_task(author_client, task_id):
    url = reverse('tasks:confirm_delete', args=task_id)
    form_data = {'confirm-delete': 'confirm-delete'}
    response = author_client.post(url, data=form_data)

    assertRedirects(response, reverse('tasks:task_list'))
    assert Task.objects.count() == 0


def test_not_author_cant_delete_task(not_author_client, task_id):
    url = reverse('tasks:confirm_delete', args=task_id)
    form_data = {'confirm-delete': 'confirm-delete'}
    response = not_author_client.post(url, data=form_data)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Task.objects.count() == 1

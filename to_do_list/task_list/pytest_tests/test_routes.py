import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_cases import fixture_ref, parametrize
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'page, expected_status',
    (
        ('tasks:task_list', HTTPStatus.FOUND),
        ('tasks:add_task', HTTPStatus.FOUND)
    )
)
def test_pages_availability_for_anon_user(client, page, expected_status):
    url = reverse(page)
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'page',
    ('tasks:task_list', 'tasks:add_task')
)
def test_pages_availability_for_auth_user(author_client, page):
    url = reverse(page)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@parametrize(
    'client, expected_status',
    (
        (fixture_ref('author_client'), HTTPStatus.OK),
        (fixture_ref('not_author_client'), HTTPStatus.NOT_FOUND)
    )
)
@parametrize(
    'page',
    ('tasks:task', 'tasks:confirm_delete')
)
def test_pages_availability_for_different_users(task, client, expected_status, page):
    url = reverse('tasks:task', args=(task.id,))
    response = client.get(url)
    assert response.status_code == expected_status


@parametrize(
    'name, args',
    (
        ('tasks:task_list', None),
        ('tasks:add_task', None),
        ('tasks:task', fixture_ref('task_id')),
        ('tasks:confirm_delete', fixture_ref('task_id')),
    )
)
def test_redirects(client, name, args):
    login_url = reverse('login')
    url = reverse(name, args=args)

    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)

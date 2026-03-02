from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects


def test_anon_user_redirect(client):
    url = reverse('user_profile:profile')
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'

    response = client.get(url)
    assertRedirects(response, expected_url)


def test_auth_user_exit(author_client):
    url = reverse('logout')
    response = author_client.post(url)
    assert response.status_code == HTTPStatus.OK


def test_auth_user_password_change(author_client):
    url = reverse('user_profile:profile')
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_auth_user_cancel_redirect(author_client):
    url = reverse('user_profile:profile')
    expected_url = reverse('homepage:index')
    response = author_client.post(url, {'cancel': 'Отмена'})

    assertRedirects(response, expected_url)

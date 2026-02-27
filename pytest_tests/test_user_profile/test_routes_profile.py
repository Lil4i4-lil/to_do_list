import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_cases import fixture_ref, parametrize
from pytest_django.asserts import assertRedirects


def test_anon_user_redirect(client):
    url = reverse('user_profile:profile')
    login_url = reverse('login')
    expected_url = f'{login_url}?next={url}'

    response = client.get(url)
    assertRedirects(response, expected_url)


def test_auth_user_cancel_redirect(author_client):
    url = reverse('user_profile:profile')
    expected_url = reverse('homepage:index')
    response = author_client.post(url, {'cancel': 'Отмена'})

    assertRedirects(response, expected_url)


@pytest.mark.django_db
def test_password_change_link_redirects(author_client):
    profile_url = reverse('user_profile:profile')

    response = author_client.get(profile_url)
    content = response.content.decode()

    password_change_url = reverse('password_change')

    assert password_change_url in content

    redirect_response = author_client.get(password_change_url)

    assert redirect_response.status_code == 200

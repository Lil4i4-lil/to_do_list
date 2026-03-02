import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from http import HTTPStatus
from pytest_cases import fixture_ref, parametrize


@parametrize(
    'client',
    (fixture_ref('client'), fixture_ref('author_client'))
)
def test_homepage_availability_for_different_users(client):
    url = reverse('homepage:index')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_homepage_redirect_to_task_list(author_client):
    url = reverse('homepage:index')
    response = author_client.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    redirection_link = soup.find('a', attrs={'name': 'redirection'}).get('href')

    redirect_response = author_client.get(redirection_link)
    assert redirect_response.status_code == HTTPStatus.OK

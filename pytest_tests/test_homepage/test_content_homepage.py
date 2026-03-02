from django.urls import reverse
from bs4 import BeautifulSoup
from pytest_cases import fixture_ref, parametrize


@parametrize(
    'client, link_in',
    (
            (fixture_ref('client'), False),
            (fixture_ref('author_client'), True),
    )
)
def test_link_to_task_list_on_page_for_different_users(client, link_in):
    url = reverse('homepage:index')
    response = client.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    redirection_link = soup.find('a', attrs={'name': 'redirection'})

    assert (not redirection_link is None) == link_in


def test_auth_user_username_on_page(author, author_client):
    url = reverse('homepage:index')
    response = author_client.get(url)
    content = response.content.decode()
    assert author.username in content


def test_auth_user_task_count_on_page(author, author_client, author_task_count):
    url = reverse('homepage:index')
    response = author_client.get(url)

    assert 'task_count' in response.context
    assert response.context['task_count'] == author_task_count

    content = response.content.decode()
    assert str(author_task_count) in content

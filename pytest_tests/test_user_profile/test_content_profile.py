from django.urls import reverse

from user_profile.forms import ProfileForm


def test_page_contains_form(author_client):
    url = reverse('user_profile:profile')
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], ProfileForm)


def test_page_contains_password_change_link(author_client):
    url = reverse('user_profile:profile')

    response = author_client.get(url)
    content = response.content.decode()

    password_change_url = reverse('password_change')
    assert password_change_url in content

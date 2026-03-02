import pytest
from http import HTTPStatus
from django.urls import reverse
from datetime import date


@pytest.mark.parametrize(
    'button, value, is_changed',
    (
        ('save', 'Save', True),
        ('cancel', 'Cancel', False),
    )
)
def test_user_can_edit_profile_info(author, author_client, profile_form_data, button, value, is_changed):
    url = reverse('user_profile:profile')
    profile_form_data[button] = value
    response = author_client.post(url, profile_form_data)

    assert response.status_code == HTTPStatus.FOUND

    author.refresh_from_db()

    assert (author.username == profile_form_data['username']) == is_changed
    assert (author.email == profile_form_data['email']) == is_changed
    assert (author.phone_number == profile_form_data['phone_number']) == is_changed
    assert (author.first_name == profile_form_data['first_name']) == is_changed
    assert (author.last_name == profile_form_data['last_name']) == is_changed
    # assert (date.strftime(author.birthday, '%Y-%m-%d') == profile_form_data['birthday']) == is_changed

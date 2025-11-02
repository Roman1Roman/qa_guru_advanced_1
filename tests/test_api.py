from http import HTTPStatus

import pytest
import requests
from requests import Response
from models.User import User
from models.Pagination import Pagination


@pytest.fixture()
def get_users(get_app_url) -> dict:
    response: Response = requests.get(f'{get_app_url}/users/')
    assert response.status_code == HTTPStatus.OK
    return response.json().get('items')


def test_users(get_app_url) -> None:
    response: Response = requests.get(f'{get_app_url}/users/')
    assert response.status_code == HTTPStatus.OK

    users = response.json().get('items')
    for user in users:
        assert User.model_validate(user)


@pytest.mark.parametrize('user_id', [1, 6, 12])
def test_user(get_app_url, user_id) -> None:
    response: Response = requests.get(f'{get_app_url}/users/{user_id}')
    assert response.status_code == HTTPStatus.OK

    user = response.json()
    assert User.model_validate(user)


@pytest.mark.parametrize('user_id', [13])
def test_nonexistent_user(get_app_url, user_id) -> None:
    response: Response = requests.get(f'{get_app_url}/users/{user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('user_id', [0, -1, 'test'])
def test_invalid_user(get_app_url, user_id) -> None:
    response: Response = requests.get(f'{get_app_url}/users/{user_id}')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_users_no_duplicates(get_users) -> None:
    users_ids = [user_id.get('id') for user_id in get_users]
    print(users_ids)
    assert len(users_ids) == len(set(users_ids))


def test_pagination_model(get_app_url) -> None:
    response: Response = requests.get(f'{get_app_url}/users?page=1&size=1')
    assert response.status_code == HTTPStatus.OK
    assert Pagination.model_validate(response.json())


@pytest.mark.parametrize('page, size, objects_expected', [
    (1, 5, 5),
    (3, 5, 2),
])
def test_users_object_count(get_app_url, page, size, objects_expected) -> None:
    response: Response = requests.get(f'{get_app_url}/users?page={page}&size={size}')
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('size') == size
    assert response.json().get('page') == page
    assert len(response.json().get('items')) == objects_expected


@pytest.mark.parametrize('size, pages_expected', [
    (1, 12),
    (2, 6),
    (12, 1),
])
def test_user_pages(get_app_url, size, pages_expected) -> None:
    response: Response = requests.get(f'{get_app_url}/users?size={size}')
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('size') == size
    assert response.json().get('pages') == pages_expected


@pytest.mark.parametrize('page, size_expected', [
    (1, 12),
    (2, 0),
])
def test_user_object_size(get_app_url, page, size_expected) -> None:
    response: Response = requests.get(f'{get_app_url}/users?page={page}')
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('page') == page
    assert len(response.json().get('items')) == size_expected

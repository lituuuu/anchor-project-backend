from test.mock import user_mock
from api import user
import pytest

def test_register_success(mocker):
    json = {'username': 'my_test', 'email': 'my_test', 'password': 'my_test'}
    mocker.patch(
        'api.db.user.User.insert',
        return_value=user_mock.user_mock_insert(json)
    )
    test_class = user.register(json)
    assert test_class.username == "my_test"

def test_register_error(mocker):
    with pytest.raises(Exception):
        json = {'username': 'my_test', 'email': 'my_test', 'password': 'my_test'}
        mocker.patch(
            'api.db.user.User.insert',
            return_value=user_mock.internal_server_error()
        )
        user.register(json)

def test_login_success(mocker):
    json = {'username': 'my_test', 'email': 'my_test', 'password': 'my_test'}
    mocker.patch(
        'api.db.user.User.get_by_username',
        return_value=user_mock.user_mock_get(json)
    )
    mocker.patch(
        'main.bcrypt.check_password_hash',
        return_value=True
    )
    test_class = user.login(json)
    assert test_class.token.decode('UTF-8') == user_mock.user_encode_jwt

def test_login_error(mocker):
    with pytest.raises(Exception):
        json = {'username': 'my_test', 'email': 'my_test', 'password': 'my_test'}
        mocker.patch(
            'api.db.user.User.get_by_username',
            return_value=user_mock.not_found_error()
        )
        user.login(json)






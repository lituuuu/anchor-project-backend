from tests.mock import user_mock
from api import user

def test_register_success(mocker):
    mocker.patch(
        'api.model.user_model.insert',
        return_value=user_mock.user_mock_insert
    )
    variavel = json={'login': 'teste', 'email': 'teste@teste.teste', 'password': 'teste'}
    temp = user.register(variavel)
    assert temp == True

def test_register_error(mocker):
    mocker.patch(
        'api.model.user_model.insert',
        return_value=False
    )
    variavel = json={'login': 'teste', 'email': 'teste@teste.teste', 'password': 'teste'}
    temp = user.register(variavel)
    assert temp == False

def test_login_success(mocker):
    mocker.patch(
        'api.model.user_model.get',
        return_value=user_mock.user_mock_get
    )
    variavel = json={'login': 'teste', 'email': 'teste@teste', 'password': 'teste'}
    temp = user.login(variavel)
    assert temp == user_mock.user_encode_jwt

def test_login_error(mocker):
    mocker.patch(
        'api.model.user_model.get',
        return_value=user_mock.user_mock_get_error
    )
    variavel = json={'login': 'teste', 'email': 'teste@teste', 'password': 'teste'}
    temp = user.login(variavel)
    assert temp == None


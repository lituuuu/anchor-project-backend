from main import app

def test_ping():
    response = app.test_client().get('/ping')

    assert response.status_code == 200

def test_validateJwt_error():
    response = app.test_client().get('/validatejwt')

    assert response.status_code == 401

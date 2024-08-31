import pytest
import jwt
from decouple import config

from app.schemas import UserReturn, Token

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')


def test_creation_and_delete_user(client):
    response = client.post('/users/', json={'email': 'liquid_ice@gmail.com', 'username': 'uwu_nyashka_uwu', 'password': 'ogyrech_molochko'})
    user = UserReturn(**response.json())
    assert user.email == 'liquid_ice@gmail.com'
    assert user.username == 'uwu_nyashka_uwu'
    assert response.status_code == 201


def test_login(test_user, client):
    response = client.post('/login', data={'username': test_user['username'], 'password': test_user['password']})
    token_response = Token(**response.json())
    payload = jwt.decode(token_response.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get('user_id')

    assert id == test_user['id']
    assert token_response.token_type == 'bearer'
    assert response.status_code == 200


@pytest.mark.parametrize('username, password', [
    ('uwu_nyashka_uwu', 'fakepasswordheheheha'),
    ('Yeager', 'ohyeahitsthereference'),
    ('q', 'w')
])
def test_incorrect_login(test_user, client, username, password):
    response = client.post('/login', data={'username': username, 'password': password})
    assert response.status_code == 403
    assert response.json().get('detail') == 'Invalid credentials'
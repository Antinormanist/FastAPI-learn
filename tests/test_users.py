from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_noob():
    response = client.get('/')
    assert response.json().get('Hello') == 'Corigi was here'
    assert response.status_code == 200


def test_creation_user():
    response = client.post('/users', json={'email': 'liquid_ice@gmail.com', 'username': 'uwu_nyashka_uwu', 'password': 'ogyrech_molochko'})
    response = response.json()
    print(response)
    assert response.get('email') == 'liquid_ice@gmail.com'
    assert response.get('username') == 'uwu_nyashka_uwu'
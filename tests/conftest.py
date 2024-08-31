import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from decouple import config
from app.routers.auth import create_access_token


DB = config('DB')
DB_USER = config('DB_USER')
DB_USER_PSWRD = config('DB_USER_PSWRD')
DB_HOST = config('DB_HOST_TEST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')

engine = create_engine(f'{DB}://{DB_USER}:{DB_USER_PSWRD}@{DB_HOST}:{DB_PORT}/{DB_NAME}_test', echo=True)
TestSessionLocal = sessionmaker(engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {'email': 'liquid_ice@gmail.com', 'username': 'uwu_nyashka_uwu', 'password': 'ogyrech_molochko'}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {'email': 'qliquid_ice@gmail.com', 'username': 'quwu_nyashka_uwu', 'password': 'ogyrech_molochko'}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user, client):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({
        'Authorization': f'Bearer {token}'}
    )
    return client


@pytest.fixture
def create_post(authorized_client):
    response = authorized_client.post('/posts/', json={'title': 'Should we hate furries?', 'content': 'I ate a banana'})
    return response.json()

from venv import create

from app.routers.auth import create_access_token


def test_get_all_posts(authorized_client, create_post):
    response = authorized_client.get('/posts/')
    assert response.status_code == 200


def test_get_post(authorized_client, create_post):
    response = authorized_client.get(f'/posts/{create_post['id']}')
    assert response.status_code == 200
    assert response.json()['title'] == create_post['title']
    assert response.json()['content'] == create_post['content']


def test_unauthorized_create_post(client):
    response = client.post('/posts/', json={
        'title': 'qwe',
        'content': 'qwe'
    })
    assert response.status_code == 401


def test_delete_post(authorized_client, create_post):
    response = authorized_client.delete(f'/posts/{create_post['id']}')
    assert response.status_code == 204


def test_invalid_delete_post(authorized_client):
    response = authorized_client.delete('/posts/2024')
    assert response.status_code == 404
    assert response.json()['detail'] == 'post with id: 2024 is not found'


def test_unauthorized_delete_post(client, create_post):
    client.headers.pop('authorization')
    response = client.delete(f'/posts/{create_post['id']}')
    assert response.status_code == 401


def test_delete_another_user_post(client, create_post, test_user2):
    token = create_access_token({'user_id': test_user2['id']})
    client.headers['Authorization'] = f'Bearer {token}'
    response = client.delete(f'/posts/{create_post['id']}')
    assert response.status_code == 403


def test_update_post(authorized_client, create_post):
    response = authorized_client.put(f'/posts/{create_post['id']}', json={
        'title': 'Pineapple',
        'content': 'I bought a very cool cat',
        'is_published': False
    })
    assert response.status_code == 200
    assert response.json()['title'] == 'Pineapple'
    assert response.json()['content'] == 'I bought a very cool cat'
    assert response.json()['is_published'] == False


def test_invalid_update_post(authorized_client):
    response = authorized_client.put('/posts/2024', json={
        'title': 'Pineapple',
        'content': 'I bought a very cool cat',
        'is_published': False
    })
    assert response.status_code == 404


def test_unauthorized_update_post(create_post, client):
    client.headers.pop('authorization')
    response = client.put(f'/posts/{create_post['id']}', json={
        'title': 'Pineapple',
        'content': 'I bought a very cool cat',
        'is_published': False
    })
    assert response.status_code == 401


def test_another_user_update_post(client, create_post, test_user2):
    token = create_access_token({'user_id': test_user2['id']})
    client.headers['Authorization'] = f'Bearer {token}'
    response = client.put(f'/posts/{create_post['id']}', json={
        'title': 'Pineapple',
        'content': 'I bought a very cool cat',
        'is_published': False
    })
    assert response.status_code == 403
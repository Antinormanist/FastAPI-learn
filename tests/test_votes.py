def test_vote_on_post(authorized_client, create_post):
    response = authorized_client.post('/vote', json={'post_id': create_post['id'], 'dir': 1})
    assert response.status_code == 201


def test_double_vote_on_post(authorized_client, create_post):
    authorized_client.post('/vote', json={'post_id': create_post['id'], 'dir': 1})
    response = authorized_client.post('/vote', json={'post_id': create_post['id'], 'dir': 0})
    assert response.status_code == 409


def test_vote_on_invalid_post(authorized_client):
    response = authorized_client.post('/vote', json={'post_id': '2024', 'dir': 1})
    assert response.status_code == 404


def test_unauthorized_vote_on_post(client, create_post):
    client.headers.pop('Authorization')
    response = client.post('/vote', json={'post_id': create_post['id'], 'dir': 1})
    assert response.status_code == 401
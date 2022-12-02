def test_create_ads(client, user_token):
    response = client.get('/create/')
    assert response.status_code == 201
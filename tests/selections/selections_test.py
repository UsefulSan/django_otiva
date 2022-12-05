import pytest

from tests.factories import AdFactory


@pytest.mark.django_db
def test_create_selection(client, user_login):
    ads = AdFactory.create()
    expected_response = {
        "id": 1,
        "items": [ads.pk],
        "owner": user_login['id'],
        "name": "test"
    }
    response = client.post('/ads/selections/create/', data={
        'items': [ads.pk],
        'name': 'test'
    }, content_type="application/json", HTTP_AUTHORIZATION="Bearer " + user_login['token'])
    assert response.status_code == 201
    assert response.data == expected_response

import json

import pytest


from ads.models import Categories
from ads.serializers import AdDetailViewSerializer
from tests.factories import AdFactory
from users.models import Users


@pytest.mark.django_db
def test_create_ads(client, user_token):
    cat = Categories.objects.create(name='testovaya')
    expected_response = {
        "id": 1,
        "category": cat.pk,
        "author": 1,
        "is_published": False,
        "name": "Стол из слэба и эпоксидной смолы",
        "price": 24000,
        "description": None,
        "image": None
    }
    response = client.post('/ads/create/', data={
        "name": "Стол из слэба и эпоксидной смолы",
        "author": 1,
        "price": 24000,
        "category": cat.pk
    }, HTTP_AUTHORIZATION="Bearer " + user_token)
    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list_ads(client):
    ads = AdFactory.create_batch(21)
    expected_response = {
        "items": AdDetailViewSerializer(ads, many=True).data,
        "page": 1,
        "num_pages": 3,
        "total": 21
    }
    response = client.get('/ads/', safe=False)
    jsonresponse = {'items': response.json().get('items'), }
    assert response.status_code == 200
    assert response == expected_response

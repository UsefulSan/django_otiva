import pytest

from ads.models import Categories
from ads.serializers import AdListViewSerializer, AdDetailViewSerializer
from tests.factories import AdFactory


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
    ads = AdFactory.create_batch(10)
    expected_response = {
        "count": 10,
        "next": None,
        "previous": None,
        "results": AdListViewSerializer(ads, many=True).data
    }
    response = client.get('/ads/', safe=False)
    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve_ads(client, user_token):
    ad = AdFactory.create()
    expected_response = AdDetailViewSerializer(ad).data
    response = client.get(f'/ads/{ad.pk}/', HTTP_AUTHORIZATION="Bearer " + user_token)
    assert response.status_code == 200
    assert response.data == expected_response

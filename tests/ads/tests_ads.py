import pytest


def test_a():
    assert True

@pytest.mark.django_db
def test_rabotaet(client):
    response = client.get('/ads/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_ads(client, ads, user_token):
    expected_response = {
            "id": ads.id,
            "name": "Стол из слэба и эпоксидной смолы",
            "author": "Петр",
            "price": 24000,
            "description": "",
            "is_published": False,
            "image": "",
            "category": "Мебель и интерьер"
        }
    response = client.post('/create/', data={
            "name": "Стол из слэба и эпоксидной смолы",
            "author": "Петр",
            "price": 24000,
            "category": "Мебель и интерьер"
        }, HTTP_AUTHORIZATION="Bearer " + user_token)

    assert response.status_code == 201
    assert response.data == expected_response

    # @pytest.mark.django_db
    # def test_create_vacancy(client, hr_token):
    #     expected_response = {
    #         "slug": "123",
    #         "name": "123"
    #     }
    #
    #     Skill.objects.create(name="test")
    #     response = client.post("/vacancy/create/", data={
    #         "slug": "123",
    #         "name": "123"
    #     }, HTTP_AUTHORIZATION="Token " + hr_token)
    #
    #     assert response.status_code == 201
    #     assert response.data == expected_response



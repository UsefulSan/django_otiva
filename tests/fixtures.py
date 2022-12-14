import pytest


@pytest.fixture()
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = 'dragon84'
    password = 'sasha123456'

    django_user_model.objects.create_user(username=username, password=password, role='member')
    response = client.post('/users/login/', {'username': username, 'password': password}, format='json')

    return response.data["access"]


@pytest.fixture()
@pytest.mark.django_db
def user_login(client, django_user_model):
    username = 'dragon84'
    password = 'sasha123456'

    user = django_user_model.objects.create_user(username=username, password=password, role='member')
    response = client.post('/users/login/', {'username': username, 'password': password}, format='json')

    return {'token': response.data["access"], 'id': user.pk}

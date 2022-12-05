import factory.django

from ads.models import Ads, Categories
from users.models import Users


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    username = factory.Faker('name')
    password = 'passwordTestFactory'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories

    name = factory.Faker('name')


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ads

    name = factory.Faker('name')
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    is_published = False
    price = 100

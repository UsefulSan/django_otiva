import factory.django

from ads.models import Ads


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ads

    name = factory.Faker('name')
    author = 'author'
    price = 100
    is_published = False
    image = '1234'
    category = 'Котики'

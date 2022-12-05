from pytest_factoryboy import register

from tests.factories import AdFactory

pytest_plugins = 'tests.fixtures'

register(AdFactory)

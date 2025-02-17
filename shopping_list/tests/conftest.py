import pytest

from shopping_list.models import ShoppingList, ShoppingItem


@pytest.fixture(scope='session')
def create_shopping_item():
    def _create_shopping_item(name):
        shopping_list = ShoppingList.objects.create(name='Foo')
        shopping_item = ShoppingItem.objects.create(shopping_list=shopping_list, name=name, purchased=False)
        return shopping_item

    return _create_shopping_item

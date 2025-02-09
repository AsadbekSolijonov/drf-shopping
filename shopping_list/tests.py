from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shopping_list.models import ShoppingList, ShoppingItem


# POST LIST HAPPY
@pytest.mark.django_db
def test_valid_shopping_list_is_created():
    url = reverse('all-shopping-lists')
    data = {
        "name": "Foobar"
    }
    client = APIClient()
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingList.objects.get().name == "Foobar"


# POST LIST UNHAPPY
def test_shopping_list_name_missing_returns_bad_request():
    url = reverse("all-shopping-lists")
    data = {
        "something_name": "blablabla"
    }
    client = APIClient()
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# GET ALL LIST HAPPY
@pytest.mark.django_db
def test_get_all_shopping_lists():
    url = reverse("all-shopping-lists")
    client = APIClient()
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


# RETRIVE LIST HAPPY
@pytest.mark.django_db
def test_retrive_shopping_list():
    shopping_list = ShoppingList.objects.create(name="Foobar")
    url = reverse("shopping-list-detail", args=[shopping_list.id])
    client = APIClient()
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == str(shopping_list.id)
    assert response.data['name'] == 'Foobar'


# PUT LIST HAPPY
@pytest.mark.django_db
def test_update_shopping_list():
    shopping_list = ShoppingList.objects.create(name='Foobar')
    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()
    data = {
        "name": "Foo"
    }
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == str(shopping_list.id)
    assert response.data['name'] == 'Foo'


# PUT LIST UNHAPPY
@pytest.mark.django_db
def test_update_shopping_list_missing_name():
    shopping_list = ShoppingList.objects.create(name='Foobar')
    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()
    data = {
        "something_name": "Foo"
    }
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_shopping_list():
    shopping_list = ShoppingList.objects.create(name='Foobar')
    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_create_shopping_item():
    shopping_list = ShoppingList.objects.create(name="Foobar")
    url = reverse("shopping-items-create", args=[shopping_list.id])
    client = APIClient()
    data = {
        "name": "Bazz"
    }
    response = client.post(url, data, format="json")  # format="json" qo'shib yuborilsa xatolik beryapti nima uchun?

    assert response.status_code == status.HTTP_201_CREATED  # assert 201 == 201   but  => => (assert 400 == 201)

    SHOPPING_ITEM = ShoppingItem.objects.get()
    assert SHOPPING_ITEM.name == "Bazz"
    assert SHOPPING_ITEM.purchased == False
    assert SHOPPING_ITEM.shopping_list == shopping_list


@pytest.mark.django_db
def test_update_shopping_item():
    shopping_list = ShoppingList.objects.create(name="Foobar")
    shopping_item = ShoppingItem.objects.create(name="BarBuz", purchased=False, shopping_list_id=shopping_list.id)
    url = reverse("shopping-items-detail", args=[shopping_list.id, shopping_item.id])
    client = APIClient()
    data = {
        "name": "Corage",
        "purchased": True
    }
    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK

    SHOPPING_ITEM = ShoppingItem.objects.get()
    assert SHOPPING_ITEM.name == "Corage"
    assert SHOPPING_ITEM.purchased == True
    assert SHOPPING_ITEM.shopping_list == shopping_list


@pytest.mark.django_db
def test_delete_shopping_item():
    shopping_list = ShoppingList.objects.create(name="Foobar")
    shopping_item = ShoppingItem.objects.create(name="BarBuz", purchased=False, shopping_list_id=shopping_list.id)
    url = reverse("shopping-items-detail", args=[shopping_list.id, shopping_item.id])
    client = APIClient()
    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

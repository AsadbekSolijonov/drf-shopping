from django.test import TestCase

# Create your tests here.
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shopping_list.models import ShoppingList, ShoppingItem


# ======================== LIST SHoppingList ========================
# GET ALL LIST (HAPPY PATH)
@pytest.mark.django_db
def test_all_shopping_lists_are_listed():
    """
    Bu testda shoppinglist ni List [] ro'yxati tekshirildi, Shoppingitemlarsiz.
    """
    ShoppingList.objects.create(name="Foo")
    ShoppingList.objects.create(name="Bar")

    url = reverse("all-shopping-lists")
    client = APIClient()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['name'] == 'Foo'
    assert response.data[1]['name'] == 'Bar'


# ======================== RETRIEVE SHoppingList ========================

# GET RETRIVE LIST (HAPPY PATH)
@pytest.mark.django_db
def test_shopping_list_is_retrieved_by_id():
    """
    Bu testda shoppinglist ni o'zini detail holatini tekshirildi. Shoppingitemlarsiz.
    """
    shopping_list = ShoppingList.objects.create(name="Foobar")

    url = reverse("shopping-list-detail", args=[shopping_list.id])
    client = APIClient()

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Foobar'


@pytest.mark.django_db
def test_shopping_list_includes_only_corresponding_items():
    """
    Bu testda shoppinglist va shoppingitem ni ichma-ich to'g'ri bog'langanligi testlandi.
    """
    shopping_list = ShoppingList.objects.create(name="Foo")
    another_shopping_list = ShoppingList.objects.create(name='Bar')

    ShoppingItem.objects.create(shopping_list=shopping_list, name='Buz', purchased=False)
    ShoppingItem.objects.create(shopping_list=another_shopping_list, name='Tik', purchased=False)

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()

    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['shopping_items']) == 1
    assert response.data['shopping_items'][0]['name'] == 'Buz'


# ======================== UPDATE SHoppingList ========================

# PUT Shoppinglit (HAPPY PATH)
@pytest.mark.django_db
def test_update_shopping_list():
    """
    Shoppinglistni o'zini Update bo'lishini testlandi. Shoppingitemsiz
    """
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


# PUT Shoppinglist (UNHAPPY PATH)
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


# PATCH ShoppingList (HAPPY PATH)
@pytest.mark.django_db
def test_shoppinglist_name_is_change_with_partial_udpdate():
    """
    Shoppinglistni Partial Upda xolatini testlandi. Shoppingitemsiz.
    """
    shopping_list = ShoppingList.objects.create(name='Foo')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()

    data = {
        "name": 'Bar'
    }

    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Bar'


# PATCH ShoppingList (UNHAPPY PATH)
@pytest.mark.django_db
def test_shoppinglist_name_is_change_with_partial_udpdate():
    """
    Shoppinglistni Partial Upda xolatini noto'g'ri maydon bilan testlandi JAVOB 200 status qaytishi kerak..
    """
    shopping_list = ShoppingList.objects.create(name='Foo')
    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()

    data = {
        "some_thing": 'BlaBlaBla'
    }

    response = client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK


# ======================== DELETE SHoppingList ========================
# DELETE ShoppingList (HAPPY PATH)
@pytest.mark.django_db
def test_shopping_list_delete():
    shopping_list = ShoppingList.objects.create(name='Foobar')

    url = reverse('shopping-list-detail', args=[shopping_list.id])
    client = APIClient()

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(ShoppingList.objects.all()) == 0


# ======================== CREATE SHoppingList ========================
# POST CREATE Shoppinglist (HAPPY PATH)
@pytest.mark.django_db
def test_valid_shopping_list_is_created():
    url = reverse('all-shopping-lists')
    client = APIClient()

    data = {
        "name": "Foobar"
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert ShoppingList.objects.get().name == "Foobar"


# POST CREATE Shoppinglist (UNHAPPY PATH)
def test_shopping_list_name_missing_returns_bad_request():
    url = reverse("all-shopping-lists")
    client = APIClient()

    data = {
        "something_name": "blablabla"
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ======================== CREATE SHoppingItem ========================
# POST CREATE Shoppingitem (HAPPY PATH)
@pytest.mark.django_db
def test_valid_shopping_item_is_created():
    shopping_list = ShoppingList.objects.create(name="Foobar")

    url = reverse("shopping-items-create", args=[shopping_list.id])
    client = APIClient()

    data = {
        "name": "Bazz",
        'purchased': False
    }

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_valid_shopping_item_missing_data_returns_bad_request():
    shopping_list = ShoppingList.objects.create(name="Foobar")

    url = reverse("shopping-items-create", args=[shopping_list.id])
    client = APIClient()

    data = {
        "name": "Bazz",
    }
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# ======================== RETRIEVE SHoppingItem ========================
@pytest.mark.django_db
def test_shopping_item_is_retrieved_by_id(create_shopping_item):
    """
    ShoppingItem ni batavsil tekshirish. Bunda fixture ni session scope orqali testlandi.
    """
    shopping_item = create_shopping_item(name='Chocolate')

    url = reverse('shopping-items-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Chocolate'


# ======================== UPDATE SHoppingItem ========================
# HAPPY PATH
@pytest.mark.django_db
def test_change_shopping_item_purchased_status(create_shopping_item):
    shopping_item = create_shopping_item(name='Coco')

    url = reverse("shopping-items-detail", kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()

    data = {
        "name": "Choco",
        "purchased": True
    }

    response = client.put(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert ShoppingItem.objects.get().purchased is True


# UNHAPPY PATH
@pytest.mark.django_db
def test_change_shopping_item_status_with_missing_data_returns_bad_request(create_shopping_item):
    shopping_item = create_shopping_item(name='Coco')

    url = reverse('shopping-items-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()

    data = {
        'purchased': True
    }

    response = client.put(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# PATCH HAPPY PATH
@pytest.mark.django_db
def test_change_shopping_item_purchased_status_with_partial_update(create_shopping_item):
    shopping_item = create_shopping_item(name='Coco')

    url = reverse('shopping-items-detail', kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()

    data = {
        'purchased': True
    }

    response = client.patch(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert ShoppingItem.objects.get().purchased is True


# ======================== DELETE SHoppingItem ========================
@pytest.mark.django_db
def test_shopping_item_is_deleted(create_shopping_item):
    shopping_item = create_shopping_item(name='Coco')

    url = reverse("shopping-items-detail", kwargs={'pk': shopping_item.shopping_list.id, 'item_pk': shopping_item.id})
    client = APIClient()

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(ShoppingItem.objects.all()) == 0

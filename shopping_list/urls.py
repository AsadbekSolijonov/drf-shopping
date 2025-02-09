from django.urls import path, include
from rest_framework import routers

from shopping_list.api.views import ListAddShoppingList, ShoppingListDetail, AddShoppingItem, ShoppingItemDetail

urlpatterns = [
    path('shopping-lists/', ListAddShoppingList.as_view(), name="all-shopping-lists"),
    path('shopping-lists/<uuid:pk>/', ShoppingListDetail.as_view(), name='shopping-list-detail'),
    path('shopping-lists/<uuid:pk>/shopping-items/', AddShoppingItem.as_view(), name='shopping-items'),
    path('shopping-lists/<uuid:pk>/shopping-items/<uuid:item_pk>/', ShoppingItemDetail.as_view(),
         name='shopping-items-detail'),
]

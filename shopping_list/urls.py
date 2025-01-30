from django.urls import path, include
from rest_framework import routers

from shopping_list.api.viewsets import ShoppingItemViewSet, ShoppingListViewSet

router = routers.DefaultRouter()
router.register("shopping-items", ShoppingItemViewSet, basename="shopping-items")
router.register("shopping-list", ShoppingListViewSet, basename="shopping-list")

urlpatterns = [
    path('', include(router.urls))
]

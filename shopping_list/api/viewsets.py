from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shopping_list.api.serializers import ShoppingItemSerializer, ShoppingListSerializer
from shopping_list.models import ShoppingItem, ShoppingList


class ShoppingItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer

    @action(detail=False, methods=['DELETE'], url_path="delete-all-purchased", url_name="delete-all-purchased")
    def delete_purchased(self, request):
        ShoppingItem.objects.filter(purchased=True).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['PATCH'], url_path="mark-bulk-purchased", url_name="mark-bulk-purchased")
    def mark_bulk_purchased(self, request):
        try:
            queryset = ShoppingItem.objects.filter(id__in=request.data["shopping_items"])
            queryset.update(purchased=True)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Purchased Succesfully!"}, status=status.HTTP_200_OK)


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    @action(detail=True, methods=["POST"], url_path="add-list-items", url_name="add-list-items")
    def add_items(self, request, pk=None):
        shopping_list = self.get_object()
        item_datas = request.data.get("shopping_items", [])
        for item_data in item_datas:
            ShoppingItem.objects.create(shopping_list=shopping_list, **item_data)
        return Response({"message": "Items added successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"], url_path="update-items", url_name="update-items")
    def update_items(self, request, pk=None):
        shopping_list = self.get_object()
        item_datas = request.data.get('shopping_items', [])
        shopping_list.shopping_items.all().delete()
        for item_data in item_datas:
            ShoppingItem.objects.create(shopping_list=shopping_list, **item_data)
        return Response({'message': "Items Updated Succesfully"}, status=status.HTTP_200_OK)


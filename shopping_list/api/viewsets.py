from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from shopping_list.api.serializers import ShoppingItemSerializer
from shopping_list.models import ShoppingItem


class ShoppingItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer

    @action(detail=False, methods=['DELETE'], url_path="delete-all_purchased", url_name="delete-all-purchased")
    def delete_purchased(self, request):
        ShoppingItem.objects.filter(purchased=True).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['PATCH'], url_path="mark-bulk-purchased", url_name="mark-bulk-purchased")
    def mark_bulk_purchased(self, request):
        try:
            print(request.data.get("shopping_items"))
            queryset = ShoppingItem.objects.filter(id__in=request.data["shopping_items"])
            queryset.update(purchased=True)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

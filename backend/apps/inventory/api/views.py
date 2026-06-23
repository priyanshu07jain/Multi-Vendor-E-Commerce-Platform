from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.exceptions import (
    ValidationError
)

from apps.catalog.selectors.product_selector import (
    ProductSelector
)

from apps.catalog.models import (
    ProductVariant
)

from apps.inventory.services.inventory_service import (
    InventoryService
)

from apps.inventory.selectors.inventory_selector import (
    InventorySelector
)

from apps.inventory.selectors.inventory_transaction_selector import (
    InventoryTransactionSelector
)

from .serializers import (
    StockInSerializer,
    InventorySerializer,
    InventoryTransactionSerializer,
)




class InventoryAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        variant_id
    ):

        variant = ProductVariant.objects.get(
            id=variant_id
        )

        inventory = (
            InventorySelector.get_inventory_by_variant(
                variant
            )
        )

        if not inventory:

            return Response(
                {
                    "detail": "Inventory not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = (
            InventorySerializer(
                inventory
            )
        )

        return Response(
            serializer.data
        )
    


class StockInAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        variant_id
    ):

        variant = ProductVariant.objects.get(
            id=variant_id
        )

        serializer = (
            StockInSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        inventory, _ = (
            Inventory.objects.get_or_create(
                variant=variant
            )
        )

        inventory = (
            InventoryService.add_stock(
                inventory_id=inventory.id,
                quantity=serializer.validated_data[
                    "quantity"
                ],
                note=serializer.validated_data.get(
                    "note",
                    ""
                ),
            )
        )

        return Response(
            InventorySerializer(
                inventory
            ).data
        )
    
class InventoryTransactionAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        variant_id
    ):

        variant = ProductVariant.objects.get(
            id=variant_id
        )

        inventory = (
            InventorySelector.get_inventory_by_variant(
                variant
            )
        )

        if not inventory:

            return Response(
                []
            )

        transactions = (
            InventoryTransactionSelector
            .get_inventory_transactions(
                inventory
            )
        )

        serializer = (
            InventoryTransactionSerializer(
                transactions,
                many=True
            )
        )

        return Response(
            serializer.data
        )
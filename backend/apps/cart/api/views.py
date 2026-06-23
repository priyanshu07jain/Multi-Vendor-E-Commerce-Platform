from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)

from apps.cart.selectors.cart_selector import (
    CartSelector,
)

from apps.cart.services.cart_service import (
    CartService,
)

from apps.catalog.models import (
    ProductVariant,
)

from .serializers import (
    CartItemSerializer,
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
)

class CartAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        cart = (
            CartSelector.get_user_cart(
                request.user
            )
        )

        items = (
            cart.items
            .select_related(
                "variant"
            )
            .all()
        )

        serializer = (
            CartSerializer(
                {
                    "id": cart.id,
                    "items": items,
                }
            )
        )

        return Response(
            serializer.data
        )
    

class CartItemAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        cart = (
            CartSelector.get_user_cart(
                request.user
            )
        )

        serializer = (
            CartItemCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        variant = (
            ProductVariant.objects.get(
                id=serializer.validated_data[
                    "variant_id"
                ]
            )
        )

        item = (
            CartService.add_item(
                cart=cart,
                variant=variant,
                quantity=serializer.validated_data[
                    "quantity"
                ]
            )
        )

        return Response(
            CartItemSerializer(
                item
            ).data,
            status=status.HTTP_201_CREATED,
        )
    

class CartItemDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        item_id
    ):

        cart = (
            CartSelector.get_user_cart(
                request.user
            )
        )

        item = (
            CartSelector.get_cart_item(
                cart=cart,
                item_id=item_id,
            )
        )

        serializer = (
            CartItemUpdateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        item = (
            CartService.update_quantity(
                item=item,
                quantity=serializer.validated_data[
                    "quantity"
                ]
            )
        )

        return Response(
            CartItemSerializer(
                item
            ).data
        )

    def delete(
        self,
        request,
        item_id
    ):

        cart = (
            CartSelector.get_user_cart(
                request.user
            )
        )

        item = (
            CartSelector.get_cart_item(
                cart=cart,
                item_id=item_id,
            )
        )

        CartService.remove_item(
            item=item
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    

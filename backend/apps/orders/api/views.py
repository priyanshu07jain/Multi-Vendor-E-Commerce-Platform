from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)

from apps.cart.selectors.cart_selector import (
    CartSelector,
)

from apps.orders.selectors.order_selector import (
    OrderSelector,
)

from apps.orders.services.order_service import (
    OrderService,
)

from .serializers import (
    OrderSerializer,
)



class CheckoutAPIView(
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

        orders = (
            OrderService.checkout(
                cart=cart
            )
        )

        serializer = (
            OrderSerializer(
                orders,
                many=True
            )
        )

        return Response(
            serializer.data
        )
    


class OrderListAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        orders = (
            OrderSelector.get_user_orders(
                request.user
            )
        )

        serializer = (
            OrderSerializer(
                orders,
                many=True
            )
        )

        return Response(
            serializer.data
        )
    

class OrderDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        order_id
    ):

        order = (
            OrderSelector.get_order_by_id(
                user=request.user,
                order_id=order_id,
            )
        )

        serializer = (
            OrderSerializer(
                order
            )
        )

        return Response(
            serializer.data
        )
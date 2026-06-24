from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework import status

from apps.addresses.selectors.address_selector import (
    AddressSelector,
)

from apps.addresses.services.address_service import (
    AddressService,
)

from .serializers import (
    AddressSerializer,
    AddressCreateSerializer,
    AddressUpdateSerializer,
)


class AddressAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        addresses = (
            AddressSelector.get_user_addresses(
                request.user
            )
        )

        serializer = (
            AddressSerializer(
                addresses,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    def post(
        self,
        request
    ):

        serializer = (
            AddressCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        address = (
            AddressService.create_address(
                user=request.user,
                **serializer.validated_data
            )
        )

        return Response(
            AddressSerializer(
                address
            ).data,
            status=status.HTTP_201_CREATED,
        )


class AddressDetailAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        address_id
    ):

        address = (
            AddressSelector.get_user_address(
                user=request.user,
                address_id=address_id,
            )
        )

        serializer = (
            AddressUpdateSerializer(
                address,
                data=request.data,
                partial=True,
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        address = (
            AddressService.update_address(
                address=address,
                **serializer.validated_data
            )
        )

        return Response(
            AddressSerializer(
                address
            ).data
        )

    def delete(
        self,
        request,
        address_id
    ):

        address = (
            AddressSelector.get_user_address(
                user=request.user,
                address_id=address_id,
            )
        )

        AddressService.delete_address(
            address=address
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
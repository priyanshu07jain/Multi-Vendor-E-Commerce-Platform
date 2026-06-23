from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.vendors.models import Vendor
from .serializers import VendorCreateSerializer

from apps.vendors.services.vendor_service import VendorService
from apps.vendors.api.serializers import VendorSerializer, VendorMemberSerializer

from apps.vendors.selectors.vendor_selector import VendorSelector
from rest_framework.exceptions import ValidationError

from .serializers import MemberCreateSerializer
from .serializers import (
    VendorCreateSerializer,
    VendorSerializer,
    VendorMemberSerializer,
    MemberCreateSerializer,
    MemberRoleUpdateSerializer,
)


class VendorCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = VendorCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        vendor = VendorService.create_vendor(
            user=request.user, **serializer.validated_data
        )

        return Response(
            {
                "id": str(vendor.id),
                "name": vendor.name,
                "slug": vendor.slug,
            },
            status=status.HTTP_201_CREATED,
        )


class VendorListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        vendors = VendorSelector.get_user_vendors(request.user)

        serializer = VendorSerializer(vendors, many=True)

        return Response(serializer.data)


class VendorDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):

        vendor = VendorSelector.get_user_vendor_by_id(
            user=request.user,
            vendor_id=vendor_id,
        )

        serializer = VendorSerializer(vendor)

        return Response(serializer.data)


class VendorMemberAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        vendor_id
    ):

        vendor = (
            VendorSelector.get_user_vendor_by_id(
                user=request.user,
                vendor_id=vendor_id,
            )
        )

        serializer = (
            MemberCreateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            membership = (
                VendorService.add_member(
                    actor=request.user,
                    vendor=vendor,
                    **serializer.validated_data
                )
            )

        except ValueError as e:

            raise ValidationError(
                str(e)
            )

        return Response(
            {
                "id": str(membership.id),
                "user": membership.user.email,
                "role": membership.role,
            },
            status=status.HTTP_201_CREATED
        )

    def get(
        self,
        request,
        vendor_id
    ):

        vendor = (
            VendorSelector.get_user_vendor_by_id(
                user=request.user,
                vendor_id=vendor_id,
            )
        )

        memberships = (
            VendorSelector.get_vendor_members(
                vendor
            )
        )

        serializer = (
            VendorMemberSerializer(
                memberships,
                many=True
            )
        )

        return Response(
            serializer.data
        )

    def patch(
        self,
        request,
        vendor_id,
        membership_id
    ):

        vendor = (
            VendorSelector.get_user_vendor_by_id(
                user=request.user,
                vendor_id=vendor_id,
            )
        )

        membership = (
            VendorSelector.get_vendor_membership(
                vendor=vendor,
                membership_id=membership_id,
            )
        )

        serializer = (
            MemberRoleUpdateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            membership = (
                VendorService.update_member_role(
                    actor=request.user,
                    membership=membership,
                    **serializer.validated_data
                )
            )

        except ValueError as e:

            raise ValidationError(
                str(e)
            )

        return Response(
            {
                "id": str(membership.id),
                "email": membership.user.email,
                "role": membership.role,
            }
        )
    

    def delete(
    self,
    request,
    vendor_id,
    membership_id
    ):
        vendor = (
        VendorSelector.get_user_vendor_by_id(
            user=request.user,
            vendor_id=vendor_id,
        )
        )

        membership = (
        VendorSelector.get_vendor_membership(
            vendor=vendor,
            membership_id=membership_id,
        )
        )

        try:

         VendorService.remove_member(
            actor=request.user,
            membership=membership,
        )

        except ValueError as e:

         raise ValidationError(
            str(e)
        )

        return Response(
        status=status.HTTP_204_NO_CONTENT
    )
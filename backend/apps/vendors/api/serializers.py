from rest_framework import serializers
from apps.vendors.models import (
    MembershipRole,
)

class VendorCreateSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=255
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )
    
    
class VendorSerializer(
    serializers.Serializer
):
    id = serializers.UUIDField(
        read_only=True
    )

    name = serializers.CharField(
        read_only=True
    )

    slug = serializers.CharField(
        read_only=True
    )

    description = serializers.CharField(
        read_only=True
    )

    is_active = serializers.BooleanField(
        read_only=True
    )
    
    
class MemberCreateSerializer(
    serializers.Serializer
):

    email = serializers.EmailField()

    role = serializers.ChoiceField(
        choices=MembershipRole.choices
    )
    
class VendorMemberSerializer(
    serializers.Serializer
):

    id = serializers.UUIDField(
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    role = serializers.CharField(
        read_only=True
    )
    
class MemberRoleUpdateSerializer(
    serializers.Serializer
):

    role = serializers.ChoiceField(
        choices=MembershipRole.choices
    )
from rest_framework import serializers
from apps.users.models import User
from apps.users.services.user_service import UserService


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate_email(self, value):

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate_username(self, value):

        if User.objects.filter(
            username=value
        ).exists():

            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def create(
        self,
        validated_data
    ):

        return UserService.create_user(
            **validated_data
        )
        


class UserSerializer(
    serializers.Serializer
):

    id = serializers.UUIDField(
        read_only=True
    )

    username = serializers.CharField(
        read_only=True
    )

    email = serializers.EmailField(
        read_only=True
    )
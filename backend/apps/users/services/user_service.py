from apps.users.models import User


from django.db import transaction

from apps.users.models import (
    User,
    Role,
    UserRole,
)


class UserService:

    @staticmethod
    @transaction.atomic
    def create_user(
        username,
        email,
        password,
    ):

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        customer_role = Role.objects.get(
            name="CUSTOMER"
        )

        UserRole.objects.create(
            user=user,
            role=customer_role,
        )

        return user
from django.shortcuts import get_object_or_404

from apps.users.models import User


class UserSelector:

    @staticmethod
    def get_user_by_email(
        email
    ):
        return get_object_or_404(
            User,
            email=email
        )
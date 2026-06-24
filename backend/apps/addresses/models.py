from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User


class Address(BaseModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    full_name = models.CharField(
        max_length=255
    )

    phone_number = models.CharField(
        max_length=20
    )

    address_line_1 = models.CharField(
        max_length=255
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    country = models.CharField(
        max_length=100
    )

    postal_code = models.CharField(
        max_length=20
    )

    is_default = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = "addresses"

    def __str__(self):
        return (
            f"{self.full_name} - {self.city}"
        )
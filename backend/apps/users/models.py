

from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.common.models import BaseModel


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    is_email_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.username


class Role(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Permission(BaseModel):
    code = models.CharField(
    max_length=100,
    unique=True,
    db_index=True
)

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.code


class UserRole(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_roles"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_users"
    )

    class Meta:
     constraints = [
        models.UniqueConstraint(
            fields=["user", "role"],
            name="unique_user_role"
        )
    ]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class RolePermission(BaseModel):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="permission_roles"
    )

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role.name} - {self.permission.code}"
from django.db import models

from apps.common.models import BaseModel
from apps.users.models import User

class Vendor(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    slug = models.SlugField(
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name
    
    
    
    
class MembershipRole(models.TextChoices):
    OWNER = "OWNER", "Owner"
    MANAGER = "MANAGER", "Manager"
    EMPLOYEE = "EMPLOYEE", "Employee"
    
    
    
class VendorMembership(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="vendor_memberships"
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="members"
    )

    role = models.CharField(
        max_length=20,
        choices=MembershipRole.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "vendor"],
                name="unique_vendor_membership"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.vendor.name} ({self.role})"
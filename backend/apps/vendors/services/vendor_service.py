from django.db import transaction
from django.utils.text import slugify

from apps.vendors.models import (
    Vendor,
    VendorMembership,
    MembershipRole,
)

from django.db import transaction

from apps.users.models import User

class VendorService:

    @staticmethod
    @transaction.atomic
    def create_vendor(
        user,
        name,
        description=""
    ):

        slug = slugify(name)

        vendor = Vendor.objects.create(
            name=name,
            slug=slug,
            description=description,
        )

        VendorMembership.objects.create(
            user=user,
            vendor=vendor,
            role=MembershipRole.OWNER,
        )

        return vendor
    

    @staticmethod
    @transaction.atomic
    def add_member(
    *,
    actor,
    vendor,
    email,
    role,
    ):

     actor_membership = VendorMembership.objects.get(
        user=actor,
        vendor=vendor,
    )

     if actor_membership.role == MembershipRole.EMPLOYEE:
        raise ValueError(
            "Employees cannot add members."
        )

     if (
        actor_membership.role == MembershipRole.MANAGER
        and role != MembershipRole.EMPLOYEE
    ):
        raise ValueError(
            "Managers can only add employees."
        )

     user = User.objects.get(
        email=email
    )

     if VendorMembership.objects.filter(
        user=user,
        vendor=vendor,
    ).exists():

        raise ValueError(
            "User is already a member."
        )

     membership = VendorMembership.objects.create(
        user=user,
        vendor=vendor,
        role=role,
    )

     return membership 
 
     
    @staticmethod
    @transaction.atomic
    def update_member_role(
    *,
    actor,
    membership,
    role,
    ):

     actor_membership = (
        VendorMembership.objects.get(
            user=actor,
            vendor=membership.vendor,
        )
    )

     if actor_membership.role != MembershipRole.OWNER:
        raise ValueError(
    "Only owners can change roles."
)

     membership.role = role

     membership.save(
    update_fields=["role"]
)

     return membership
 
    
@staticmethod
@transaction.atomic
def remove_member(
    *,
    actor,
    membership,
):

    actor_membership = (
        VendorMembership.objects.get(
            user=actor,
            vendor=membership.vendor,
        )
    )

    if actor_membership.role != MembershipRole.OWNER:
        raise ValueError(
            "Only owners can remove members."
        )

    if membership.role == MembershipRole.OWNER:

        owner_count = (
            VendorMembership.objects.filter(
                vendor=membership.vendor,
                role=MembershipRole.OWNER,
            ).count()
        )

        if owner_count <= 1:
            raise ValueError(
                "Vendor must have at least one owner."
            )

    membership.delete()
    
    
    
    
    

  
from django.db import models

from apps.common.models import BaseModel
from apps.vendors.models import Vendor

# Create your models here.
class Category(BaseModel):
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

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name
    
    
    


class Product(BaseModel):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name = models.CharField(
        max_length=255
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
    
    
    
    


class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    name = models.CharField(
        max_length=255
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.name}"
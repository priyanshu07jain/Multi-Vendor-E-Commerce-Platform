from django.contrib import admin

from apps.vendors.models import Vendor, VendorMembership

# Register your models here.
admin.site.register(Vendor)
admin.site.register(VendorMembership)
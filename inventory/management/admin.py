from django.contrib import admin
from .models import Brand, Device, Company

# Register your models here.

try:
    company = Company.objects.first()
    admin_header = company.name + " Inventory Management "
except:
    admin_header = "Inventory Management "


admin.site.index_title = admin_header
admin.site.site_header = admin_header + 'Admin Page'
admin.site.site_title = admin_header

class DeviceAdmin(admin.ModelAdmin):
    model = Device

    list_display = (
        'brand',
        'serial_number',
        'status',
        'location',
        'model',
        'remarks'
    )

    search_fields = [
        'location',
        'remarks',
        'model',
        'serial_number'
    ]
    
    list_filter = (
        'brand',
        'status',
    )

admin.site.register(Company)
admin.site.register(Brand)
admin.site.register(Device, DeviceAdmin)
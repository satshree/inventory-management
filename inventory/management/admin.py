from django.contrib import admin
from .models import Brand, Device

# Register your models here.

admin.site.index_title = 'Mercantile Communication Network Operation Control (MCNOC) Inventory Management'
admin.site.site_header = 'MCNOC Inventory Management Admin Page'
admin.site.site_title = 'MCNOC Inventory Management'

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

admin.site.register(Brand)
admin.site.register(Device, DeviceAdmin)
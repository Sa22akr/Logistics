from django.contrib import admin
from .models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'sender_name', 'receiver_name', 'status', 'created_at')
    search_fields = ('tracking_number', 'sender_name', 'receiver_name')
    list_filter = ('status', 'created_at')
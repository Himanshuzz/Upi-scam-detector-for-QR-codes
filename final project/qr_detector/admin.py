from django.contrib import admin
from .models import QRScanResult

@admin.register(QRScanResult)
class QRScanResultAdmin(admin.ModelAdmin):
    list_display = ("id", "upi_id", "risk_level", "created_at")
    list_filter = ("risk_level", "created_at")
    search_fields = ("upi_id", "decoded_text")

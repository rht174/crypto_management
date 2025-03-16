from django.contrib import admin
from .models import CryptoPrice


@admin.register(CryptoPrice)
class CryptoPriceAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'price', 'org_id', 'timestamp')
    list_filter = ('symbol', 'timestamp')
    search_fields = ('symbol', 'org_id__name')
    date_hierarchy = 'timestamp'

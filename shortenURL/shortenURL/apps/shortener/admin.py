from django.contrib import admin
from .models import ShortenedURL, URLAccess

# Register your models here.

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'user', 'created_at')
    search_fields = ('short_code', 'original_url')
    list_filter = ('created_at',)

@admin.register(URLAccess)
class URLAccessAdmin(admin.ModelAdmin):
    list_display = ('shortened_url', 'ip_address', 'accessed_at')
    list_filter = ('accessed_at',)
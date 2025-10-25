from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
    list_filter = ("name", "description", "price")
    search_fields = ("name", "description")
    ordering = ("name", "price")

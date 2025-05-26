from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description']
    search_fields = ['name']
    list_filter = ['price','name']
    ordering = ['id']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'date_ordered']
    search_fields = ['date_ordered','user', 'product']
    list_filter = ['date_ordered','user', 'product']
    ordering = ['date_ordered']

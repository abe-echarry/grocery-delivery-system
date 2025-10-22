from django.contrib import admin
from .models import Category, Product, Address, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "category", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("sku", "name")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "line1", "city", "state", "zip")
    search_fields = ("user__username", "line1", "city", "zip")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "total", "address")
    list_filter = ("created_at",)
    search_fields = ("user__username", "id")
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price_each")
    search_fields = ("order__id", "product__name")

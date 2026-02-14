from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductVariant, Order, OrderItem


# 🔹 PRODUCT VARIANT INLINE (BEST WAY)
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# 🔹 PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]


# 🔹 ORDER ADMIN
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "phone",
        "utr_last6",
        "grand_total",
        "status",
        "created_at",
    )

    list_filter = ("status", "created_at")
    search_fields = ("user__username", "phone", "utr_last6")
    list_editable = ("status",)

    readonly_fields = ("payment_image_preview",)

    fieldsets = (
        ("Customer Info", {
            "fields": ("user", "name", "phone", "address")
        }),
        ("Payment Info", {
            "fields": ("utr_last6", "payment_screenshot", "payment_image_preview")
        }),
        ("Order Info", {
            "fields": ("total_price", "gst", "grand_total", "status")
        }),
    )

    def payment_image_preview(self, obj):
        if obj.payment_screenshot:
            return format_html(
                '<img src="{}" width="300" />',
                obj.payment_screenshot.url
            )
        return "No Screenshot"

    payment_image_preview.short_description = "Screenshot Preview"


# 🔹 ORDER ITEM
admin.site.register(OrderItem)

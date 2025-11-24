from django.contrib import admin

from .models import Item, Order, Discount, Tax

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    fields = ["name", "description", "price", "currency"]
    list_display = ["name", "description", "price", "currency"]
    search_fields = ["name"]


class OrderAdmin(admin.ModelAdmin):
    fields = ["items", "discount", "tax"]
    list_display = ["id", "display_items", "items_count", "discount", "tax", "total_price"]
    readonly_fields = ["total_price"]
    search_fields = ["items__name"]

    def display_items(self, obj):
        return ", ".join([item.name for item in obj.items.all()])
    
    display_items.short_description = 'Items'
    
    def items_count(self, obj):
        return obj.items.count()
    
    items_count.short_description = "Items"
    items_count.admin_order_field = "items__count"


class DiscountAdmin(admin.ModelAdmin):
    fields = ["name", "discount_percentage", "stripe_id_eur", "stripe_id_usd"]
    list_display = ["name", "discount_percentage", "stripe_id_eur", "stripe_id_usd"]
    search_fields = ["name"]


class TaxAdmin(admin.ModelAdmin):
    fields = ["name", "tax_percentage", "stripe_id_eur", "stripe_id_usd"]
    list_display = ["name", "tax_percentage", "stripe_id_eur", "stripe_id_usd"]
    search_fields = ["name"]


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)
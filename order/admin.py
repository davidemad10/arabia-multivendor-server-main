from django.contrib import admin
from .models import Order, OrderItem, ReturnRequest, ReturnRequestFile


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 
    readonly_fields = ('product', 'color', 'size', 'quantity', 'total_price', 'shipping_status')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # Prevents adding new OrderItems directly in Order
    


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created', 'is_paid', 'payment_method', 'get_total')
    list_filter = ('is_paid', 'payment_method', 'created')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('get_total', 'created', 'paid_date')
    inlines = [OrderItemInline]

    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total Price'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'total_price', 'shipping_status', 'created')
    list_filter = ('shipping_status', 'created')
    search_fields = ('product__name', 'order__user__username')
    readonly_fields = ('total_price', 'created')


class ReturnRequestFileInline(admin.TabularInline):
    model = ReturnRequestFile
    extra = 1


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_item', 'tracking_number', 'status', 'reason', 'created')
    list_filter = ('status', 'reason', 'created')
    search_fields = ('user__username', 'tracking_number', 'order_item__product__name')
    inlines = [ReturnRequestFileInline]
    readonly_fields = ('created',)


@admin.register(ReturnRequestFile)
class ReturnRequestFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'return_request', 'evidence_file')
    search_fields = ('return_request__id',)
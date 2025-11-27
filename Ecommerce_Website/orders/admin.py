from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem"""
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'price', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""
    list_display = ('order_number', 'user', 'status', 'total', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email', 'shipping_city', 'shipping_state')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'total')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax', 'shipping_cost', 'total')
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_address',
                'shipping_city',
                'shipping_state',
                'shipping_zip_code',
                'shipping_country',
                'shipping_phone'
            )
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('subtotal', 'tax', 'shipping_cost')
        return self.readonly_fields


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model"""
    list_display = ('id', 'order', 'product', 'quantity', 'price', 'subtotal', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product__name', 'product__sku')
    readonly_fields = ('subtotal', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model"""
    list_display = ('payment_id', 'order', 'amount', 'payment_method', 'payment_gateway', 'status', 'created_at', 'paid_at')
    list_filter = ('status', 'payment_method', 'payment_gateway', 'created_at')
    search_fields = ('payment_id', 'order__order_number', 'razorpay_order_id', 'razorpay_payment_id', 'order__user__username')
    readonly_fields = ('payment_id', 'created_at', 'updated_at', 'paid_at', 'gateway_response')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'order', 'amount', 'currency', 'status', 'created_at', 'updated_at', 'paid_at')
        }),
        ('Payment Method', {
            'fields': ('payment_method', 'payment_gateway')
        }),
        ('Razorpay Details', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('failure_reason', 'gateway_response'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('order', 'amount', 'currency', 'payment_method', 'payment_gateway')
        return self.readonly_fields

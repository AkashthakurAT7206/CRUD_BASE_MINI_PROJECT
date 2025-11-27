from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
import random
import string

User = get_user_model()


def generate_order_number():
    """Generate unique order number"""
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f'ORD-{timestamp}-{random_str}'


class Order(models.Model):
    """Store customer orders"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Wallet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='India')
    shipping_phone = models.CharField(max_length=15)
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()
        if not self.total:
            self.total = self.subtotal + self.tax + self.shipping_cost
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"
    
    def get_status_badge_class(self):
        """Return Bootstrap class for status badge"""
        status_classes = {
            'pending': 'warning',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger',
            'refunded': 'secondary',
        }
        return status_classes.get(self.status, 'secondary')
    
    def get_status_display_class(self):
        """Alias for get_status_badge_class for template compatibility"""
        return self.get_status_badge_class()


class OrderItem(models.Model):
    """Individual items in an order"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='order_items')
    size = models.CharField(max_length=30, blank=True, help_text="Selected size for this item")
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.subtotal:
            self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        size_label = f" ({self.size})" if self.size else ""
        return f"{self.quantity}x {self.product.name}{size_label} - Order {self.order.order_number}"


class Payment(models.Model):
    """Payment transactions for orders"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
        ('manual', 'Manual'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Unique payment transaction ID")
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True, help_text="Razorpay order ID")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True, help_text="Razorpay payment ID")
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True, help_text="Razorpay signature for verification")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    currency = models.CharField(max_length=3, default='INR')
    
    payment_method = models.CharField(max_length=20, choices=Order.PAYMENT_METHOD_CHOICES)
    payment_gateway = models.CharField(max_length=20, choices=PAYMENT_GATEWAY_CHOICES, default='razorpay')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment gateway response data (JSON)
    gateway_response = models.JSONField(default=dict, blank=True, null=True, help_text="Full response from payment gateway")
    
    failure_reason = models.TextField(blank=True, null=True, help_text="Reason for payment failure if any")
    
    paid_at = models.DateTimeField(null=True, blank=True, help_text="When payment was successfully completed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_id']),
            models.Index(fields=['order', '-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['razorpay_order_id']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            # Generate unique payment ID
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.payment_id = f'PAY-{timestamp}-{random_str}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Payment {self.payment_id} - Order {self.order.order_number} - {self.get_status_display()}"
    
    def get_status_badge_class(self):
        """Return Bootstrap class for status badge"""
        status_classes = {
            'pending': 'warning',
            'processing': 'info',
            'completed': 'success',
            'failed': 'danger',
            'cancelled': 'secondary',
            'refunded': 'secondary',
        }
        return status_classes.get(self.status, 'secondary')
    
    def mark_as_completed(self):
        """Mark payment as completed"""
        self.status = 'completed'
        self.paid_at = timezone.now()
        self.order.payment_status = True
        self.order.save()
        self.save()
    
    def mark_as_failed(self, reason=None):
        """Mark payment as failed"""
        self.status = 'failed'
        if reason:
            self.failure_reason = reason
        self.save()
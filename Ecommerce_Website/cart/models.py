from django.db import models
from django.contrib.auth.models import User
from products.models import Product  

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart({self.user.username})"
        return f"Cart(Session: {self.session_key})"

    def get_total_price(self):
        total = sum(item.get_total() for item in self.items.all())
        return round(total, 2)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=30, blank=True, help_text="Selected size (e.g., S, M, L)")

    class Meta:
        unique_together = ('cart', 'product', 'size')

    def __str__(self):
        size_label = f" - {self.size}" if self.size else ""
        return f"{self.product.name}{size_label} ({self.quantity})"

    def get_total(self):
        price = self.product.discount_price or self.product.price
        return round(price * self.quantity, 2)

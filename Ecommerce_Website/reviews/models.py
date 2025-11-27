from django.db import models
from django.contrib.auth.models import User
from products.models import Product  # adjust import if needed

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.user.username} ({self.rating}★)"

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"


class FeedBack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.email} - {self.subject}"


class UserAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    address_line = models.TextField()
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=120, default='India')
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} address"

    def to_order_initial(self):
        return {
            'shipping_address': self.address_line,
            'shipping_city': self.city,
            'shipping_state': self.state,
            'shipping_zip_code': self.zip_code,
            'shipping_country': self.country,
            'shipping_phone': self.phone_number,
        }
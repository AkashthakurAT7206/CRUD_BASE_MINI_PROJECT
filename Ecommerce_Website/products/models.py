from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from django.utils.text import slugify

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):   
        return self.name


# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit (Unique Product ID)")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for search")
    available_sizes = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated sizes like XS,S,M,L,XL"
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_discount_percentage(self):
        if self.discount_price and self.price > 0:
            return round(((self.price - self.discount_price) / self.price) * 100, 2)
        return 0

    def get_size_options(self):
        if not self.available_sizes:
            return []
        return [size.strip() for size in self.available_sizes.split(',') if size.strip()]

    def has_size_options(self):
        return bool(self.get_size_options())


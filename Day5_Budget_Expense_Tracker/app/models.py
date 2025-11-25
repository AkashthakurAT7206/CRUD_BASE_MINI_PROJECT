from django.db import models
from django.utils import timezone

class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
    
    class Meta:
        ordering = ['-date', '-created_at']


class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.category.name} - ₹{self.amount} ({self.month.strftime('%B %Y')})"
    
    class Meta:
        ordering = ['-month']
        unique_together = ['category', 'month']

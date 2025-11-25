from django.db import models

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-date_joined']

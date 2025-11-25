from django.db import models

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AddressBook(models.Model):
    name = models.CharField(max_length=50)
    contacts = models.ManyToManyField(Contact, related_name='address_books')
    
    def __str__(self):
        return self.name

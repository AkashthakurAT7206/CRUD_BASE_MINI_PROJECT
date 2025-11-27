
from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=200,blank=False)
    description = models.CharField(max_length=200,blank=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        # verbose = we dont have to use this
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'
    def __str__(self):
        return self.title

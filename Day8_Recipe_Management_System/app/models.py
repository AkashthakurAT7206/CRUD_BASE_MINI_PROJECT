from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):  # ✅ PascalCase
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')  # ✅ Added relationship
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')  # ✅ Added author
    
    # Remove ingredients TextField - use ManyToMany instead
    instructions = models.TextField()
    
    prep_time = models.IntegerField(help_text="Preparation time in minutes")  # ✅ Added
    cook_time = models.IntegerField(help_text="Cooking time in minutes")  # ✅ Added
    servings = models.IntegerField(default=1)  # ✅ Added
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')  # ✅ Added
    
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)  # ✅ Added
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def total_time(self):
        return self.prep_time + self.cook_time
    
    class Meta:
        ordering = ['-created_at']


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)  # ✅ Unique ingredient names
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class RecipeIngredient(models.Model):  # ✅ NEW: Through model for Recipe-Ingredient relationship
    """
    This connects Recipe and Ingredient with quantity information
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients')
    quantity = models.CharField(max_length=50, help_text="e.g., 2 cups, 100g, 1 tablespoon")
    
    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} for {self.recipe.title}"
    
    class Meta:
        unique_together = ['recipe', 'ingredient']  # Can't add same ingredient twice to a recipe


class UserProfile(models.Model):  # ✅ PascalCase
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username

from django.urls import path
from .views import (
    # Recipe URLs
    RecipeListView,
    RecipeDetailView,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    # Category URLs
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    # Ingredient URLs
    IngredientListView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
)

urlpatterns = [
    # Recipe URLs
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/update/<int:pk>/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/delete/<int:pk>/', RecipeDeleteView.as_view(), name='recipe_delete'),
    
    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # Ingredient URLs
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
    path('ingredient/create/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredient/update/<int:pk>/', IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='ingredient_delete'),
]

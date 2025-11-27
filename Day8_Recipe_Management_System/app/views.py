from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Recipe, Category, Ingredient, UserProfile
from .forms import RecipeForm, CategoryForm, IngredientForm, UserProfileForm


# Recipe Views
class RecipeListView(ListView):
    model = Recipe
    template_name = 'app/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'app/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'app/recipe_form.html'
    success_url = reverse_lazy('recipe_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'app/recipe_form.html'
    success_url = reverse_lazy('recipe_list')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


class RecipeDeleteView(UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'app/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author


# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'app/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'app/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'app/category_form.html'
    success_url = reverse_lazy('category_list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'app/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


# Ingredient Views
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'app/ingredient_list.html'
    context_object_name = 'ingredients'


class IngredientCreateView(CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'app/ingredient_form.html'
    success_url = reverse_lazy('ingredient_list')


class IngredientUpdateView(UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'app/ingredient_form.html'
    success_url = reverse_lazy('ingredient_list')


class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'app/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredient_list')
